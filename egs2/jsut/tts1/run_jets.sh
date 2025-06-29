#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

# JETS-specific configuration for Japanese TTS with maximum accent accuracy
fs=24000
n_fft=2048
n_shift=300
win_length=1200

opts=
if [ "${fs}" -eq 48000 ]; then
    # To suppress recreation, specify wav format
    opts="--audio_format wav "
else
    opts="--audio_format flac "
fi

train_set=tr_no_dev
valid_set=dev
test_sets="dev eval1"

# JETS configuration files
train_config=conf/tuning/train_jets.yaml
inference_config=conf/decode.yaml

# Use pyopenjtalk_plus_prosody for maximum accent accuracy
# This includes:
# - Pitch rise/fall markers: [ ]
# - Phrase boundaries: #
# - Pause markers: _
# - Utterance boundaries: ^ $
# - Question markers: ?
# - Improved handling with pyopenjtalk-plus
g2p=pyopenjtalk_plus_prosody

echo "Running JETS training with enhanced Japanese accent support"
echo "G2P method: ${g2p}"
echo "This provides the most detailed prosodic information for natural Japanese TTS"

./tts.sh \
    --lang jp \
    --feats_type raw \
    --fs "${fs}" \
    --n_fft "${n_fft}" \
    --n_shift "${n_shift}" \
    --win_length "${win_length}" \
    --token_type phn \
    --cleaner jaconv \
    --g2p "${g2p}" \
    --train_config "${train_config}" \
    --inference_config "${inference_config}" \
    --train_set "${train_set}" \
    --valid_set "${valid_set}" \
    --test_sets "${test_sets}" \
    --srctexts "data/${train_set}/text" \
    --tts_task gan_tts \
    --use_feats_extract false \
    --feats_extract null \
    --train_args "--init_param " \
    --g2p_train_text "data/${train_set}/text" \
    ${opts} "$@"