#!/usr/bin/env bash

set -e
set -u
set -o pipefail

log() {
    local fname=${BASH_SOURCE[1]##*/}
    echo -e "$(date '+%Y-%m-%dT%H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}
SECONDS=0

stage=0
stop_stage=100

moe_root=downloads/moe-speech-plus/data
# ↑ ここが wav や json があるフォルダのルート(あるいは train/dev/eval1 がある場所)

. utils/parse_options.sh

log "$0 $*"

# ここでは  "data/train" "data/dev" "data/eval1" をダイレクトに作る想定
# もしフォルダ構造が  moe-speech-plus/data/train/*.wav, dev/*.wav, eval1/*.wav
# になっているならこれでOK.
# もし “train/dev/eval1 にまだ分割されていない“なら、別途 subset_data_dir.sh する流れに変えてください。

if [ ${stage} -le 0 ] && [ ${stop_stage} -ge 0 ]; then
    # train
    mkdir -p data/train
    scp=data/train/wav.scp
    utt2spk=data/train/utt2spk
    text=data/train/text
    rm -f ${scp} ${utt2spk} ${text} 2>/dev/null || true

    # たとえば 下記のように train/*.wav を全部 find:
    find "${moe_root}/train" -type f -name "*.wav" | sort | while read -r fpath; do
        uttid=$(basename "${fpath}" .wav)
        echo "${uttid} ${fpath}" >> "${scp}"
        echo "${uttid} SPK1" >> "${utt2spk}"
    done
    utils/utt2spk_to_spk2utt.pl "${utt2spk}" > data/train/spk2utt

    # テキスト (anime_whisper_transcription など)
    # もし *.json 内にあるなら jq などで取り出すか、すでに “uttid transcription” の txt を作成済みならコピペしてください
    # 例として:
    for jpath in $(find "${moe_root}/train" -type f -name "*.json" | sort); do
        uttid=$(basename "${jpath}" .json)
        text_=$(jq -r '.anime_whisper_transcription' "${jpath}")
        echo "${uttid} ${text_}" >> "${text}"
    done

    utils/fix_data_dir.sh data/train
    utils/validate_data_dir.sh --no-feats data/train
fi

if [ ${stage} -le 1 ] && [ ${stop_stage} -ge 1 ]; then
    # dev
    mkdir -p data/dev
    scp=data/dev/wav.scp
    utt2spk=data/dev/utt2spk
    text=data/dev/text
    rm -f ${scp} ${utt2spk} ${text} || true

    find "${moe_root}/dev" -type f -name "*.wav" | sort | while read -r fpath; do
        uttid=$(basename "${fpath}" .wav)
        echo "${uttid} ${fpath}" >> "${scp}"
        echo "${uttid} SPK1" >> "${utt2spk}"
    done
    utils/utt2spk_to_spk2utt.pl "${utt2spk}" > data/dev/spk2utt

    for jpath in $(find "${moe_root}/dev" -type f -name "*.json" | sort); do
        uttid=$(basename "${jpath}" .json)
        text_=$(jq -r '.anime_whisper_transcription' "${jpath}")
        echo "${uttid} ${text_}" >> "${text}"
    done

    utils/fix_data_dir.sh data/dev
    utils/validate_data_dir.sh --no-feats data/dev
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    # eval1
    mkdir -p data/eval1
    scp=data/eval1/wav.scp
    utt2spk=data/eval1/utt2spk
    text=data/eval1/text
    rm -f ${scp} ${utt2spk} ${text} || true

    find "${moe_root}/eval1" -type f -name "*.wav" | sort | while read -r fpath; do
        uttid=$(basename "${fpath}" .wav)
        echo "${uttid} ${fpath}" >> "${scp}"
        echo "${uttid} SPK1" >> "${utt2spk}"
    done
    utils/utt2spk_to_spk2utt.pl "${utt2spk}" > data/eval1/spk2utt

    for jpath in $(find "${moe_root}/eval1" -type f -name "*.json" | sort); do
        uttid=$(basename "${jpath}" .json)
        text_=$(jq -r '.anime_whisper_transcription' "${jpath}")
        echo "${uttid} ${text_}" >> "${text}"
    done

    utils/fix_data_dir.sh data/eval1
    utils/validate_data_dir.sh --no-feats data/eval1
fi

log "Successfully finished data preparation. [elapsed=${SECONDS}s]"
