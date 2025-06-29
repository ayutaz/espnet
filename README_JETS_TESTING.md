# JETS Japanese TTS Testing Guide

This document describes the testing framework for JETS Japanese TTS, following t-wada's TDD principles.

## Overview

The testing suite ensures high-quality Japanese text-to-speech synthesis using JETS (Jointly Training FastSpeech2 and HiFi-GAN).

## Test Categories

### 1. Unit Tests
- **Core JETS functionality** (`test/espnet2/gan_tts/jets/test_jets.py`)
  - Model initialization
  - Forward/backward passes
  - Multi-speaker support
  - GPU compatibility

- **Japanese G2P tests** (`test/espnet2/gan_tts/jets/test_jets_japanese.py`)
  - Prosody symbol generation
  - Accent markers
  - Question intonation
  - Edge cases (empty text, special characters)

### 2. Integration Tests
- **Data pipeline validation**
  - Text preprocessing with jaconv
  - G2P conversion with pyopenjtalk-plus
  - Token mapping consistency
  
- **Mini training test** (`test/test_jets_mini_training.sh`)
  - Verifies end-to-end training capability
  - Uses minimal data for quick validation

### 3. CI/CD Tests
GitHub Actions workflow (`.github/workflows/jets_japanese_test.yml`):
- Runs on push/PR for JETS-related changes
- Tests multiple Python versions (3.8, 3.9)
- Validates Japanese G2P functionality
- Checks configuration files

## Local Testing

### Setup with uv

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv .venv-jets-test
source .venv-jets-test/bin/activate

# Install dependencies
uv pip install -r requirements_jets_test.txt
```

### Running Tests

```bash
# Run all JETS tests
pytest test/espnet2/gan_tts/jets/ -v

# Run Japanese-specific tests
pytest test/espnet2/gan_tts/jets/test_jets_japanese.py -v

# Run local G2P test
python test/test_japanese_g2p_local.py

# Run mini training test
bash test/test_jets_mini_training.sh
```

## Key Testing Principles (t-wada TDD)

1. **Test First**: Write tests before implementation
2. **Red-Green-Refactor**: 
   - RED: Write failing test
   - GREEN: Make it pass with minimal code
   - REFACTOR: Improve code quality

3. **Focus Areas**:
   - Japanese-specific issues (accent, prosody)
   - Data consistency
   - Edge case handling
   - Performance metrics

## Test Coverage

The tests cover:

1. **Phoneme Conversion**
   - Basic phoneme extraction
   - Prosody symbols (^, $, [, ], #, _, ?)
   - Accent patterns
   - Various text inputs

2. **Model Training**
   - Initialization
   - Forward/backward passes
   - Loss calculation
   - Inference

3. **Data Pipeline**
   - Text normalization
   - G2P conversion
   - Token mapping
   - Batch creation

## Continuous Integration

The GitHub Actions workflow runs automatically on:
- Push to jets-japanese-accent-fix, jets, or master branches
- Pull requests affecting JETS components
- Manual trigger via GitHub UI

## Troubleshooting

### Common Issues

1. **pyopenjtalk installation fails**
   - Install system dependencies: `sudo apt-get install mecab libmecab-dev`
   - Use pre-built wheels if available

2. **pyopenjtalk-plus not found**
   - This is optional; tests will fall back to standard pyopenjtalk
   - Install manually: `pip install pyopenjtalk-plus`

3. **Memory issues during testing**
   - Reduce batch size in test configurations
   - Use CPU-only torch for CI: `torch==1.13.0+cpu`

## Future Improvements

1. Add audio quality metrics (MCD, PESQ)
2. Implement A/B testing framework
3. Add more edge cases for Japanese text
4. Create performance benchmarks
5. Add integration with espnet_model_zoo

## References

- [t-wada's TDD principles](https://github.com/twada)
- [ESPnet documentation](https://espnet.github.io/espnet/)
- [JETS paper](https://arxiv.org/abs/2203.16852)
- [pyopenjtalk-plus](https://github.com/kaiidams/pyopenjtalk-plus)