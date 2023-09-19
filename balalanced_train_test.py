import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--scored_anno_file', type=str, required=True, help='Path to the Scored annotation file')
parser.add_argument('-t', '--train', type=str, required=True, help='Train file ')
parser.add_argument('-d', '--dev', type=str, required=True, help='Dev file ')
parser.add_argument('-e', '--eval', type=str, required=True, help='Test file ')
parser.add_argument('-dt', '--devt', type=str, required=True, help='Dev file for task organizers ')
parser.add_argument('-et', '--evalt', type=str, required=True, help='Test file for task organizers')

args = parser.parse_args()

scored_file = args.scored_anno_file
train_file = args.train
dev_file = args.dev
test_file = args.eval
devt_file = args.devt
testt_file = args.evalt



df_final = pd.read_csv(scored_file,sep='\t')
# Get nth Item for train/dev/test (we need twice as many as dev for test, hence we have test1 and test 2)
# This results rsomehow 80:8:12 split, if you need more dev/test split, start from 7/8 or 9
dev = df_final.iloc[::10]
test1 = df_final.iloc[::11]
test2 = df_final.iloc[::12]
print("Lengthis of Indices of nth elements", len(dev), len(test1), len(test2))

# Now get unique indices, some of the nth elements might be common amnongst test and dev splits
dev_only = set(dev.index.tolist())- (set(test1.index.tolist()).union(set(test2.index.tolist())))
test1_only = set(test1.index.tolist())- (set(dev.index.tolist()).union(set(test2.index.tolist())))
test2_only = set(test2.index.tolist())- (set(dev.index.tolist()).union(set(test1.index.tolist())))
print("Sizes of dev and test", len(dev_only),len(test2_only) + len(test1_only),", resp")

# remove the nth items from the original dataframe, but on the copy
train = df_final.copy()
train.drop(index=dev_only, inplace=True)
train.drop(index=test1_only, inplace=True)
train.drop(index=test2_only, inplace=True)
print("Size of train", len (train), "All elements in the original dataframe", len(df_final))

print (len(dev_only) + len(test2_only) + len(test1_only) + len(train) == len(df_final))

# now get the train and test elements
dev =  df_final.iloc[list(dev_only)]
test = df_final.iloc[list(set(test1_only).union(test2_only))]

# round two decimal places
train['score'] = round(train['score'], 2)
dev['score'] = round(dev['score'], 2)
test['score'] = round(test['score'], 2)


# Now shuffle the files before writing
train = train.sample(frac=1).reset_index(drop=True)
dev = dev.sample(frac=1).reset_index(drop=True)
test = test.sample(frac=1).reset_index(drop=True)


# Now, generate unique ID per train/dev/test
train['PairID'] = ["Pair_ID_amh_train_"+ str(i) for i in range(1, len(train)+1)]
dev['PairID'] = ["Pair_ID_amh_dev_"+ str(i) for i in range(1, len(dev)+1)]
test['PairID'] = ["Pair_ID_amh_test_"+ str(i) for i in range(1, len(test)+1)]

# are we still consistent with the total number of the data
print ("The total number of the data =", len(train) + len(dev) + len (test))
print("Tarin = ", round((len(train)/len(df_final)*100),2),"%")
print("Dev = ", round((len(dev)/len(df_final)*100),2),"%")
print("Test = ", round((len(test)/len(df_final)*100),2),"%")

#Rename column item to Text, so it is the same as the shared task format
train.rename(columns={'item': 'Text'}, inplace=True)
dev.rename(columns={'item': 'Text'}, inplace=True)
test.rename(columns={'item': 'Text'}, inplace=True)

# Repalce new line with Tab
train['Text'] = train['Text'].apply(lambda x: x.replace("\\n","\t"))
dev['Text'] = dev['Text'].apply(lambda x: x.replace("\\n","\t"))
test['Text'] = test['Text'].apply(lambda x: x.replace("\\n","\t"))

# Write to a file
train[["PairID","Text","score"]].to_csv(train_file,index=False)
dev[["PairID","Text"]].to_csv(dev_file,index=False)
test[["PairID","Text"]].to_csv(test_file,index=False)

# test and dev for task organizers
dev[["PairID","Text","score"]].to_csv(devt_file,index=False)
test[["PairID","Text","score"]].to_csv(testt_file,index=False)
