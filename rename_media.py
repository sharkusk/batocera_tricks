import os
import shutil
import argparse
from pathlib import Path

# Default file endings and their corresponding destination folders
FILE_ENDINGS = {
    'invoice': 'Invoices',
    'receipt': 'Receipts',
    'contract': 'Contracts',
    'photo': 'Photos',
    'screenshot': 'Screenshots',
    'report': 'Reports',
    # Add more file endings and destinations as needed
}

def get_top_subdir(base_path, file_path):
    """Get the topmost subdirectory relative to base path"""
    try:
        rel_path = file_path.parent.relative_to(base_path)
        parts = rel_path.parts
        return parts[0] if parts else None
    except ValueError:
        return None

def process_files(base_dir, dest_base=None, include_subdir=False, symlink=False, dry_run=False):
    base_path = Path(base_dir).resolve()
    dest_base_path = Path(dest_base).resolve() if dest_base else base_path
    
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            filepath = Path(root) / filename
            
            # Skip if not a file (e.g., symlinks)
            if not filepath.is_file():
                continue
            
            # Check if the filename contains a '-'
            if '-' in filename:
                # Split the filename into parts
                base_part, ending_part = filename.rsplit('-', 1)
                
                # Remove file extension from the ending part to get the key
                ending_key = os.path.splitext(ending_part)[0].lower()
                
                # Check if this ending is in our FILE_ENDINGS table
                if ending_key in FILE_ENDINGS:
                    # Start building destination path
                    dest_folder = dest_base_path
                    
                    # Include topmost subdirectory if requested
                    if include_subdir:
                        top_subdir = get_top_subdir(base_path, filepath)
                        if top_subdir:
                            dest_folder = dest_folder / top_subdir
                    
                    # Add the file type directory
                    dest_folder = dest_folder / FILE_ENDINGS[ending_key]
                    
                    # Get the original file extension
                    file_ext = os.path.splitext(filename)[1]
                    
                    # Construct new filename (base_part + original extension)
                    new_filename = f"{base_part}{file_ext}"
                    
                    # Full paths for source and destination
                    src_path = filepath
                    dest_path = dest_folder / new_filename
                    
                    try:
                        if dry_run:
                            print(f"[DRY RUN] Would process: {src_path} -> {dest_path}")
                            if not dest_folder.exists():
                                print(f"[DRY RUN] Would create directory: {dest_folder}")
                            continue
                        
                        # Create destination folder if it doesn't exist (only if not dry-run)
                        dest_folder.mkdir(parents=True, exist_ok=True)
                        
                        if symlink:
                            # Create symbolic link
                            if dest_path.exists():
                                print(f"Warning: Destination exists, skipping: {dest_path}")
                                continue
                            os.symlink(src_path, dest_path)
                            print(f"Created symlink: {src_path} -> {dest_path}")
                        else:
                            # Move the file
                            shutil.move(str(src_path), str(dest_path))
                            print(f"Moved: {src_path} -> {dest_path}")
                    except Exception as e:
                        print(f"Error processing {src_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Organize files based on their endings.")
    parser.add_argument('base_dir', nargs='?', default=os.getcwd(),
                       help='Base directory to search (default: current directory)')
    parser.add_argument('--dest-base', default=None,
                       help='Base destination directory (default: same as base_dir)')
    parser.add_argument('--include-subdir', action='store_true',
                       help='Include topmost subdirectory in destination path')
    parser.add_argument('--symlink', action='store_true',
                       help='Create symbolic links instead of moving files')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    
    args = parser.parse_args()
    
    print("Starting file organization...")
    print(f"Base directory: {args.base_dir}")
    print(f"Destination base: {args.dest_base if args.dest_base else '(same as base)'}")
    print(f"Include top subdir: {args.include_subdir}")
    print(f"Create symlinks: {args.symlink}")
    print(f"Dry run: {args.dry_run}")
    print("---")
    
    process_files(
        base_dir=args.base_dir,
        dest_base=args.dest_base,
        include_subdir=args.include_subdir,
        symlink=args.symlink,
        dry_run=args.dry_run
    )
    
    print("File organization complete.")

if __name__ == "__main__":
    main()
