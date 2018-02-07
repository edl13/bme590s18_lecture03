import glob
import pandas as pd
import re


def main():
    filenames = collect_csv_files()
    student_data = cat_data(filenames)
    check_teamnames(student_data)
    count_camelcase(student_data)
    write_data(student_data)


def collect_csv_files():
    # Find all csv files
    files = glob.glob('*.csv')
    return files


def cat_data(files):
    # Collect data into dataframe
    data = pd.DataFrame(columns=('First', 'Last', 'NetID', 'GitHub',
                                 'GroupName'))
    # Iterate through csv files and disregard mlp6 and everyone.csv
    # Check for commented header lines starting with '#' and create pandas
    # dataframe

    for f in files:
        if(f != 'mlp6.csv' and f != 'everyone.csv'):
            in_csv = pd.read_csv(f,
                                 skip_blank_lines=True,
                                 comment='#',
                                 names=('First', 'Last', 'NetID', 'GitHub',
                                        'GroupName'))
            data = data.append(in_csv, ignore_index=True)
    return data


def check_teamnames(data):
    # Find spaces in whitespace stripped team names
    bad_names = ''
    for i, row in data.iterrows():
        group_name = row['GroupName']
        cleaned_name = group_name.strip()
        if ' ' in cleaned_name:
            bad_names.append(' ' + cleaned_name)

    if(bad_names == ''):
        print('No spaces found in group names')
    else:
        print('Spaces found in the following group names:' + bad_names)


def count_camelcase(data):
    # Check for camelcase. Regex taken from
    # https://stackoverflow.com/questions/10182664/check-for-camel-case-in-python 
    camel_count = 0
    for i, row in data.iterrows():
        group_name = row['GroupName']
        cleaned_name = group_name.strip()
        if(re.match(r'(?:[A-Z][a-z]*)+', cleaned_name)):
            camel_count += 1
    print('{} group names found to use camel case.'.format(camel_count))


def write_data(data):
    data.to_csv('compiled.csv', index=False, header=False)
    for i, row in data.iterrows():
        netid = row['NetID']
        row.to_json(netid+'.json', orient='columns')


if __name__ == "__main__":
    main()
