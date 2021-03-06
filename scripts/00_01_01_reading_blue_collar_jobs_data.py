import pandas as pd
import datetime
# %%
output_code = "00_01_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
## Reading all the tables avaialable in the following blue collar job percentage
## website.
dataframes_from_html = pd.read_html("https://bluecollarjobs.us/2017/04/10/highest-to-lowest-share-of-blue-collar-jobs-by-state/")
df = dataframes_from_html[0]
# %%
## Now saving these percentages as a csv file

## First removing the initial row number index
df.reset_index(drop=True, inplace=True)
print(df.columns)
## Then renaming the column names
df.columns = ["state_name","blue_collar_probability","manufacturing_probability","construction_probability","mining_logging_probability"]
print(df.columns)
df = df.set_index("state_name")
# %%
def convert_string_percents_to_probability(string_percent):
    string = string_percent.replace("%","").replace("*","")
    return float(string)/100.0
# %%
for percentage_type in ["blue_collar_probability","manufacturing_probability","construction_probability","mining_logging_probability"]:
    df[percentage_type] = df[percentage_type].apply(convert_string_percents_to_probability)
# %%
df.to_csv("../data/internal/%s_blue_collar_percentages.csv" %(output_code))
# %%
## Now writing the ranking of the states based on Blue collar jobs
blue_collar_percentage_dict = df.to_dict()["blue_collar_probability"]
# %%
states_in_descending_order_based_on_blue_collarness, prob = zip(*sorted(blue_collar_percentage_dict.items(), key = lambda x: x[1], reverse = True))
states_ranked_based_on_white_collarness = map(lambda x:",".join(x),zip(reversed(states_in_descending_order_based_on_blue_collarness),map(str,range(1, len(states_in_descending_order_based_on_blue_collarness)+1))))
writelines = ["state_name,ranking_based_on_white_colarness"]
writelines.extend(states_ranked_based_on_white_collarness)
with open("../data/internal/%s_white_collarness_ranking.csv" %(output_code), "w") as f:
    f.writelines("\n".join(writelines))
    