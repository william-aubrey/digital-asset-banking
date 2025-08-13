function Get-Tree($Path, $Exclude='\.venv', $Level=0) {
    # Get all subdirectories and files in the current path.
    $items = Get-ChildItem -Path $Path -Force -ErrorAction SilentlyContinue

    # Iterate through each item.
    foreach ($item in $items) {
        # Check if the item's name matches the exclude pattern.
        if ($item.Name -notmatch $Exclude) {
            # Create a prefix for indentation.
            $prefix = "    " * $Level

            if ($item.PSIsContainer) { # It's a directory
                Write-Host "$prefix|$-- $($item.Name)"

                # Recursively call the function for the subdirectory.
                Get-Tree -Path $item.FullName -Exclude $Exclude -Level ($Level + 1)
            }
            else { # It's a file
                Write-Host "$prefix|-- $($item.Name)"
            }
        }
    }
}