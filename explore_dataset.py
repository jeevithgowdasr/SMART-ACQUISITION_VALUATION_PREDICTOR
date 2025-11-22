try:
    from datasets import load_dataset
    print("Loading dataset...")
    ds = load_dataset("gauravshrm211/VC-startup-evaluation-for-investment")
    print("Dataset loaded successfully!")
    print("Dataset info:")
    print(ds)
    
    # Check if dataset has train split
    if 'train' in ds:
        print(f"\nTrain split has {len(ds['train'])} examples")
        print("First example:")
        print(ds['train'][0])
    elif 'validation' in ds:
        print(f"\nValidation split has {len(ds['validation'])} examples")
        print("First example:")
        print(ds['validation'][0])
    else:
        # Print all available splits
        print("\nAvailable splits:")
        for split in ds.keys():
            print(f"- {split}: {len(ds[split])} examples")
            print(f"First example from {split}:")
            print(ds[split][0])
            break
            
except ImportError as e:
    print(f"Error importing datasets module: {e}")
    print("Please install it with: pip install datasets")
except Exception as e:
    print(f"Error loading dataset: {e}")