import pandas as pd


def covid_vaccine(vaccination_status_files, user_meta_file, output_file):
    """This function takes  vaccination_status_files and user_meta_file paths
    using this all the covid vaccination numbers needs to be stored in the given output file as TSV
    Args:
        vaccination_status_files: A List containing file path to the TSV vaccination_status_file.
        user_meta_file: A file path to TSV file containing User information.
        output_file: File path where output TSV results are should be stored, 
    Returns:
      None (doesnt return anything)
    """
    # your code goes here.
    #  feel free to modify this entire script, except this function signature.
    vaccination_file_data = []
    for file_path in vaccination_status_files:
        vaccination_file_data.append(pd.read_csv(file_path, sep='\t'))

    overall_vaccination_file_data = pd.concat(vaccination_file_data)
    overall_vaccination_file_data['date'] = pd.to_datetime(overall_vaccination_file_data['date'], format='%d-%m-%Y')
    filtered_overall_vaccination_file_data = overall_vaccination_file_data.query(
        "date >= '2020-02-01' and date <= '2021-11-30' "
        "and (vaccine == 'A' or vaccine == 'B' or vaccine == 'C') ")

    user_meta_file_data = pd.read_csv(user_meta_file, sep='\t')
    merged_data_vaccination_user = pd.merge(filtered_overall_vaccination_file_data, user_meta_file_data, on=['user'])
    merged_data_vaccination_user = merged_data_vaccination_user.drop('date', axis=1)
    unique_merged_data_vaccination_user = merged_data_vaccination_user.groupby(["city", "state", "vaccine", "gender"])\
        .nunique().reset_index()
    unique_merged_data_vaccination_user.columns = ['city', "state", "vaccine", "gender", "unique_vaccinated_people"]
    unique_merged_data_vaccination_user.to_csv(output_file, index=False, sep="\t")

