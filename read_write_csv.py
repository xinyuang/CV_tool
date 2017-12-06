import csv
with open('training.1600000.processed.noemoticon.csv', buffering=200000, encoding='latin-1') as f:
    csvreader = csv.reader(f, quotechar='"')
    i = 0
    for line in csvreader:
        print(line)
        #the tweet is in the last column
        #replace any " in the tweet with null
        #print(line)
        #line[-1] = line[-1].replace('"','')
        #replace any "|" in the tweet with space as "|" will be used as a delimiter later
        line[-1] = line[-1].split('|')
        #The category is in the first column
        initial_polarity = str(line[0])
        tweet = line[-1][0]
        print(initial_polarity)
        print(tweet)
        #print(type(initial_polarity))
        #print(tweet)

        if initial_polarity == '0':
            outfile = open('data/neg/' + str(i) + '.txt', 'a')
            outfile.write(tweet)
            print(line[-1][0])
            outfile.close()
        if initial_polarity == '2':
            outfile = open('data/nut/' + str(i) + '.txt', 'a')
            outfile.write(tweet)
            print(line[-1][0])
            outfile.close()
        if initial_polarity == '4':
            outfile = open('data/pos/' + str(i) + '.txt', 'a')
            outfile.write(tweet)
            print(line[-1][0])
            outfile.close()
        i = i + 1
            

    
