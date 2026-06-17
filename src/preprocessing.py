import torch
import numpy as np

print("=" * 50)
print("BCI PROJECT STARTED")
print("=" * 50)

print("PyTorch Version:", torch.__version__)
print("CUDA Available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))

sample_signal = np.random.randn(1000)

print("\nSignal Length:", len(sample_signal))
print("Mean:", np.mean(sample_signal))
print("Standard Deviation:", np.std(sample_signal))