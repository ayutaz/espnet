# JETS with Enhanced Japanese Accent Support

This branch (`jets-japanese-accent-fix`) contains improvements for Japanese TTS using JETS with better accent accuracy.

## Key Changes

1. **G2P Method**: Changed from basic `pyopenjtalk` to `pyopenjtalk_prosody`
   - Provides detailed prosodic information including:
     - Pitch rise `[` and fall `]` markers
     - Phrase boundaries `#`
     - Pause markers `_`
     - Utterance boundaries `^` (start) and `$` (end)
     - Question markers `?`

2. **Configuration**: Using JETS-specific configuration
   - `conf/tuning/train_jets.yaml` for training
   - Optimized for end-to-end text-to-waveform generation

3. **New Script**: `run_jets.sh`
   - Dedicated script for JETS training with proper options
   - Includes `--tts_task gan_tts` flag required for JETS

## Usage

### Training JETS with Enhanced Accent

```bash
# Basic training
./run_jets.sh

# Resume from stage 6 (model training)
./run_jets.sh --stage 6

# Full pipeline from data preparation
./run_jets.sh --stage 1
```

### What Each Stage Does

- Stage 1-3: Data preparation
- Stage 4: Feature extraction and text processing with prosody
- Stage 5: Token list generation
- Stage 6: JETS model training
- Stage 7: Inference/synthesis

## Example Prosody Representation

Input text: "こんにちは。"
Basic g2p: `k o N n i ch i w a`
Prosody g2p: `^ k o [ N n i ch i w a $`

The prosody markers help JETS learn:
- Natural pitch patterns
- Phrase boundaries
- Proper pausing
- Question intonation

## Expected Improvements

1. More natural Japanese accent patterns
2. Better handling of phrase boundaries
3. Improved question intonation
4. More appropriate pausing

## Notes

- The prosody-based approach requires more tokens, so training might take slightly longer
- The model can now distinguish between different prosodic contexts for the same word
- This is particularly important for Japanese where pitch accent is phonemic

## Troubleshooting

If you encounter issues:

1. Check that pyopenjtalk is properly installed:
   ```bash
   python -c "import pyopenjtalk; print(pyopenjtalk.g2p('こんにちは'))"
   ```

2. Verify the token list includes prosody symbols:
   ```bash
   cat dump/token_list/phn_jaconv_pyopenjtalk_prosody/tokens.txt | grep -E "[\[\]#\^$_?]"
   ```

3. For inference, make sure to use the same g2p setting as training.