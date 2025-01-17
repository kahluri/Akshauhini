import csv
import argparse

def extract_subdomains(input_csv, output_txt):
    with open(input_csv, 'r', encoding='utf-8') as csv_file:
        # Detect the delimiter and print the headers
        sample = csv_file.read(1024)
        csv_file.seek(0)
        dialect = csv.Sniffer().sniff(sample)
        reader = csv.DictReader(csv_file, delimiter=dialect.delimiter)

        # Print headers to check the column names
        print("Detected headers:", reader.fieldnames)

        # Collect subdomains where the status column value is 200
        subdomains = [row['subdomain'] for row in reader if 'status' in row and row['status'] == '200']
        
    # Write the subdomains to the output text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        for subdomain in subdomains:
            txt_file.write(subdomain + '\n')

def main():
    parser = argparse.ArgumentParser(description="Extract subdomains from a CSV file where status column equals 200.")
    parser.add_argument('input_csv', help="Path to the input CSV file")
    parser.add_argument('output_txt', help="Path to the output text file to save subdomains")
    
    args = parser.parse_args()
    extract_subdomains(args.input_csv, args.output_txt)
    print(f"Extracted subdomains saved to {args.output_txt}")

if __name__ == '__main__':
    main()

