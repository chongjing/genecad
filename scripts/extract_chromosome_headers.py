import argparse
import re
from collections import defaultdict
from Bio import SeqIO
import os

def extract_and_clean_headers(fasta_file):
    """Extract chromosome headers from FASTA, clean them, and handle duplicates."""
    headers = []
    seen_headers = defaultdict(int)
    
    # Extract headers from FASTA
    for record in SeqIO.parse(fasta_file, "fasta"):
        # Get header without '>' and take only characters before first space
        header = record.id.split()[0]
        headers.append(header)
    
    # Handle duplicates by appending _1, _2, _3...
    final_headers = []
    header_counts = defaultdict(int)
    
    for header in headers:
        header_counts[header] += 1
        if header_counts[header] > 1:
            final_header = f"{header}_{header_counts[header]}"
        else:
            final_header = header
        final_headers.append(final_header)
    
    return final_headers

def main():
    parser = argparse.ArgumentParser(description='Extract and clean chromosome headers from FASTA file')
    parser.add_argument('--input', required=True, help='Input FASTA file')
    parser.add_argument('--output', required=True, help='Output file with chromosome IDs')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    
    headers = extract_and_clean_headers(args.input)
    
    with open(args.output, 'w') as f:
        for header in headers:
            f.write(f"{header}\n")
    
    print(f"Extracted {len(headers)} chromosome headers to {args.output}")
    print("Headers:", ", ".join(headers[:5]) + ("..." if len(headers) > 5 else ""))

if __name__ == "__main__":
    main()
