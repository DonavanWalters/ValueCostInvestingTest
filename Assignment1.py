"""=======================================================================
 * Assignment: Assignment 1            Author: Yuhao Wang
 * Version:  001                                 
 *
 * Course:   CMPUT 175              Instructor: Choo, Euijin
 * School:   University of Alberta, Edmonton, Alberta, Canada
 * Language: Python 3.10
========================================================================"""

import codecs

class groups_produce:
    
    #initializing the file and format them into lists of strings
    def __init__(self):
        
        self.combine={}
        
        with codecs.open("WC22-YellowCards.txt", "r", "utf8") as file:
            self.content_cards=file.readlines()

        with codecs.open("WC22GroupMatches.txt", "r", "utf8") as file:
            self.content_group=file.readlines()
            
        with codecs.open("WC22Footballers.txt", "r", "utf8") as file:
            self.content_footballers=file.readlines()
    
    #print out the output on console and write in the output into files
    def print_result(self, filename, tmp_string):
        print(tmp_string)
        with open(filename, "w") as file:
            
            file.writelines(tmp_string)        
    
    #generate the text needed for groups.txt
    def text_groups(self):
        tmp_string=""
        
        for key, countries in self.combine.items():
            tmp_string += "Group " + key + "\n"
            for country in countries:
                tmp_string+=country + "\n"
            tmp_string+="\n"        
        
        return tmp_string
    
    #generate the groups.txt 
    def groups_produce(self):
        tmp_list_country=[]
        for element in self.content_footballers:
            tmp_list_country.append(element.split(" ")[0])
        country_set=set(tmp_list_country)
        
        #let the system know that the last groups should still be put into the dictionary > very important
        self.content_group.append("Terminate;Country;Country;(score)(score);date")
        
        tmp_list_combine=[]
        combine={}
        tmp_list=[]

        for element in self.content_group:
            
            element_list=element.split(";")
            
            #check if the list should still store the data into the same group or store into the dictionary and move on to storing a new group
            if element_list[0] in tmp_list or len(tmp_list)==0:
                              
                tmp_list.append(element_list[0])
                tmp_list.append(element_list[1])
                tmp_list.append(element_list[2])
                
            elif not element_list[0] in tmp_list and not len(tmp_list)==0:
                
                tmp_list_combine=list(set(tmp_list))
                tmp_list_combine.sort(key=len)
                                
                group=tmp_list_combine[0]
                
                tmp_list_combine.pop(0)
                tmp_list_combine.sort()
                
                self.combine[group]=tmp_list_combine
                
                #start of the new group
                tmp_list=[]
                tmp_list.append(element_list[0])
                tmp_list.append(element_list[1])
                tmp_list.append(element_list[2])  
            
        #print out the output
        self.print_result("groups.txt", self.text_groups())  
    
    #def generate thhe text needed for knockout.txt
    def text_knockout(self, dictionary):
        tmp_result=""
        for country_and_score in sorted(dictionary.items()):
        
            tmp_result+=f"{country_and_score[0]: <12}{country_and_score[1]: >4} pts\n"        
        return tmp_result
    
    #Order the country score:
    def order_country_score(self, item):
        
        tmp_dictionary={}
        for content in self.content_group:
            country1=content.split(";")[1]
            country2=content.split(";")[2]
          
            #check if the countries are being compared to the right data
            if country1 in item and country2 in item:
                
                #create a new storage in the dictionary for new country that hasn't been stored
                if not country1 in tmp_dictionary.keys():
                    tmp_dictionary[country1]=0
                if not country2 in tmp_dictionary.keys():
                    tmp_dictionary[country2]=0
                
                #cut the string into lists so that it is easy to compare element
                score_count_list=(content.split(";")[3]).split(')')
                #store the score to each country
                country1_score_count=len((score_count_list[0].split(',')))
                country2_score_count=len((score_count_list[1].split(",")))
                
                #check if they possibly have the same score in the game, or add points for the country that won the game
                if country1_score_count == 1 and country2_score_count ==1:
                    score_count_list[0]=score_count_list[0].replace("(", "")
                    score_count_list[1]=score_count_list[1].replace("(","")
                     
                    #check if the game ends in a draw, or check who wins
                    if len(score_count_list[0])==len(score_count_list[1]) or (not len(score_count_list[0])==0 and not len(score_count_list[1])==0):
                        
                        tmp_dictionary[country1]=tmp_dictionary[country1]+1
                        tmp_dictionary[country2]=tmp_dictionary[country2]+1  
                    
                    elif len(score_count_list[0])==0:
                            tmp_dictionary[country2]=tmp_dictionary[country2]+3    
                            
                    elif len(score_count_list[1])==0:
                            tmp_dictionary[country1]=tmp_dictionary[country1]+3
                         
                        
                elif country1_score_count<country2_score_count:
                    tmp_dictionary[country2]=tmp_dictionary[country2]+3
                    
                elif country1_score_count>country2_score_count:
                    tmp_dictionary[country1]=tmp_dictionary[country1]+3  
        return tmp_dictionary
    
    #check the score for the countries' match if they have the same point
    def check_country_match_score(self, result):
        
        for record in self.content_group:
            
            country1_score=0
            country2_score=0
            #find the match between the two country
            if result[1][0] in record and result[2][0] in record:
                
                record_score=record.split(";")[3]
                record_country1=record_score.split(")")[0]
                record_country2=record_score.split(")")[1]
                
                #check how many score each country have according to how many commas they have (does not have to be exact score)
                #or else, simply add 1 score to the respective country
                if "," in record_country1:
                    country1_score+=len(record_country1.split(","))
                
                elif not len(record_country1.replace("(", ""))==0:
                    country1_score+=1
                    
                if "," in record_country2:
                    country2_score+=len(record_country2.split(","))
                elif not len(record_country2.replace("(", ""))==0:
                    country2_score+=1        
        return country1_score, country2_score
    
    def count_yellow_cards(self, result):
        
        country1_cards=0
        country2_cards=0
        
        #compare the amount of yellow cards
        for card_string in self.content_cards:
            
            country1=result[1][0]
            country2=result[2][0]
            
            #add up the count of yellow cards for country1
            if country1 in card_string:
                
                if card_string.count(country1)==2:
                    
                    #check if it is red or yellow card
                    if card_string.split(";")[3]=="Y":
                        country1_cards+=1
                    else:
                        country1_cards+=4
            #add up the count of yellow cards for country2
            if country2 in card_string:
                if card_string.count(country2)==2:
                    
                    #check if it is red or yellow card                        
                    if card_string.split(";")[3]=="Y":
                        country2_cards+=1
                    else:
                        country2_cards+=4
        return country1_cards, country2_cards        
    
    #generate knockout.txt
    def knockout_produce(self):
        
        tmp_dictionary_combine={}
        
        for item in self.combine.values():
            
            #Order each country's score and find the top scores from each group
            tmp_dictionary=self.order_country_score(item)
                  
            #sort the data in order and store them into dictionary
            result=sorted(tmp_dictionary.items(),key=lambda x:x[1], reverse=True)
            
            tmp_dictionary_combine[result[0][0]]=result[0][1]
            
            #check if they have the same point (comparing the second and third place)
            if result[1][1]==result[2][1]:
            
                country1_score=0
                country2_score=0
                
                #check the score in order to compare them
                country1_score, country2_score=self.check_country_match_score(result)
                     
                #if the two country still have the same score then compare the count of the yellow cards
                if country1_score==country2_score:
                    
                    #find the count of the amount of yellow cards the two countries have
                    country1_cards, country2_cards=self.count_yellow_cards(result)
                    
                    #check which country has more yellow cards
                    if country1_cards>country2_cards:
                        
                        tmp_dictionary_combine[result[2][0]]=result[2][1]
                        
                    elif country2_cards>country1_cards:

                        tmp_dictionary_combine[result[1][0]]=result[1][1]        
                    
                #check which country has a higher score
                elif country1_score>country2_score:
                    tmp_dictionary_combine[result[1][0]]=result[1][1]  
                    
                else:
                    tmp_dictionary_combine[result[2][0]]=result[2][1]  
                    
            #simply store the second highest data 
            else:
                tmp_dictionary_combine[result[1][0]]=result[1][1]
                
            #initialize the dictionary for the next comparison
            tmp_dictionary.clear()
            result.clear()


        #print out the output
        self.print_result("knockout.txt", self.text_knockout(tmp_dictionary_combine))
        
    #generate text for ages.txt
    def text_ages(self, country_age, player_count):
        output_string=""
        
        for country, age in sorted(country_age.items(), key=lambda x:x[0].lower()):
            output_string+=f"{country: <12}{'{:.2f}'.format(age/player_count[country]): >5} years\n"
        
        #The overal average should be 26.93 years not 26.94 years
        output_string+=f"\nAverage Overall {'{:.2f}'.format(sum(country_age.values())/sum(player_count.values()))} years\n"
        
        return output_string
        
    #generate ages_produce    
    def ages_produce(self):
        
        country_age={}
        country_player={}
        
        for player_info in self.content_footballers:

            #store the age and country name
            country=(player_info.split(";")[0]).rsplit(" ", 1)[0]
        
            age=((player_info.split(";")[3]).split(" ")[4]).replace(")", "")
            
            #check if the country is already included in the dictionary
            if not country in country_age.keys():
                country_age[country]=0
                country_player[country]=0
            #add up the age
            country_age[country]+=int(age)
            country_player[country]+=1

        #print out the output
        self.print_result("ages.txt", self.text_ages(country_age, country_player))
    
    #generate the text for histogram.txt 
    def text_histogram(self, histogram_dictionary):
        output_string=""
        for age_key in sorted(histogram_dictionary):
            
            #check of the count is smaller than 10 for string formatting purposes
            if histogram_dictionary[age_key]<10:
                
                #check if the count is above 5 (very subtle differences)
                if histogram_dictionary[age_key]>5:
                    
                    output_string+=f"{age_key} years ( {histogram_dictionary[age_key]}) " + "*"*round(histogram_dictionary[age_key]/5) + "\n"  
                else:
                    output_string+=f"{age_key} years ( {histogram_dictionary[age_key]}) *\n"
            else:
                output_string+=f"{age_key} years ({histogram_dictionary[age_key]}) "+ "*"*round(histogram_dictionary[age_key]/5) + "\n"        
        return output_string
        
    #generate histogram.txt
    def histogram_produce(self):
        
        histogram_dictionary={}
        for age_string in self.content_footballers:
            age=int(((age_string.split(";")[3]).split(" ")[4]).replace(")", ""))
            
            #check which age group the system needs to store the count
            if age in histogram_dictionary.keys():
                histogram_dictionary[age]+=1
            else:
                histogram_dictionary[age]=1

        #print out the output
        self.print_result("histogram.txt", self.text_histogram(histogram_dictionary))
        
    #generate the text for scorer.txt
    def text_scorer(self, scorer_dictionary, player_dictionary, number_dictionary, highest_score):
        output_string="+ ------------ + ----------------- + ---------------------------------- +\n"
        
        for player_key, score_value in scorer_dictionary.items():
            
            #find the highest scoring players
            if score_value==highest_score:
                
                #check if the player number has more than two characters for formatting purposes
                if len(number_dictionary[player_key])==2:
                    output_string+=f"|  {highest_score} {'goal': <10}| {player_dictionary[player_key]: <18}| {number_dictionary[player_key] + ' ' + player_key: <35}|\n"
                else:
                    output_string+=f"|  {highest_score} {'goal': <10}| {player_dictionary[player_key]: <18}|  {number_dictionary[player_key] + ' ' + player_key: <34}|\n"
                
        output_string+="+ ------------ + ----------------- + ---------------------------------- +\n"
        return output_string
        
    def find_score_count(self, scorer_dictionary, player_country, player_number, player_name):
        for game_info in self.content_group:
            country1=game_info.split(";")[1]
            country2=game_info.split(";")[2]
            
            country1_score_list=(game_info.split(";")[3]).split(")")[0].replace("(", "").split(",")
            country2_score_list=(game_info.split(";")[3]).split(")")[1].replace("(", "").split(",")
            
            #add a new player_name into the dictionary from country2
            if country1==player_country and player_number in country1_score_list and not player_name in scorer_dictionary.keys():
                scorer_dictionary[player_name]=0
                
            #add the score count to the respective player
            if country1==player_country and player_number in country1_score_list:
                scorer_dictionary[player_name]+=country1_score_list.count(player_number)
                
            #add a new player_name into the dictionary from country2
            if country2==player_country and player_number in country2_score_list and not player_name in scorer_dictionary.keys():
                scorer_dictionary[player_name]=0
            
            #add the score count to the respective player
            if country2==player_country and player_number in country2_score_list:
                scorer_dictionary[player_name]+=country2_score_list.count(player_number)
                
        return scorer_dictionary
        
    #generate scorer.txt
    def scorer_produce(self):
        
        scorer_dictionary={}
        player_dictionary={}
        number_dictionary={}
        
        for player_info in self.content_footballers:
            player_country=player_info.split(";")[0].split(" ")[0]
            player_number=player_info.split(";")[0].split(" ")[1]
            player_name=player_info.split(';')[2]
            
            player_dictionary[player_name]=player_country
            number_dictionary[player_name]=player_number
            
            #find the score count of each place
            scorer_dictionary.update(self.find_score_count(scorer_dictionary, player_country, player_number, player_name))
          
        #sort the dictionary so that the highest value will be the first few elements of the dictionary
        result_tuple=sorted(scorer_dictionary.items(),key=lambda x:x[1], reverse=True)           
        
        
        #print out the output. Note: It is not clear how the question want us to order the output!
        self.print_result("scorer.txt", self.text_scorer(scorer_dictionary, player_dictionary, number_dictionary, result_tuple[0][1]))
    
    def count_top_yellow_cards(self, country1, country2):
        
        countries_game={}
        countries_game[country1]=0
        countries_game[country2]=0
        
        #iterate until find the desired game
        for data in self.content_cards:
            data_list=data.split(";")
                
            #find the data string needed to compare
            if f"{country1}-{country2}" in data_list or f"{country2}-{country1}" in data_list:
                
                #find the count of the yellow card of each coutry
                if country1 in data_list and "Y" in data_list:
                    countries_game[country1]+=1
                    
                elif country2 in data_list and "Y" in data_list:
                    countries_game[country2]+=1
        return countries_game

    #generate yellow.txt        
    def yellow_produce(self):
        
        record_dictionary_country={}
        for record in self.content_cards:
            countries=record.split(";")[0]
            
            #check if the country is in the dictionary yet
            if not countries in record_dictionary_country.keys():
                record_dictionary_country[countries]=1
            elif countries in record_dictionary_country.keys():
                record_dictionary_country[countries]+=1
                
        #sort the dictionary so that the highest value will be the first few elements of the dictionary
        result_tuple=sorted(record_dictionary_country.items(),key=lambda x:x[1], reverse=True)
        
        #store the highest value
        highest_cards_countries=result_tuple[0][0]
        
        country1=highest_cards_countries.split("-")[0]
        country2=highest_cards_countries.split("-")[1]
        
        #find the amount of yellow cards each country has
        countries_game=self.count_top_yellow_cards(country1, country2)
        
        output_string=f"{country1} vs {country2}\n{country1}: {countries_game[country1]} YC\n{country2}: {countries_game[country2]} YC"                
         
        #print out the output
        self.print_result("yellow.txt", output_string)

def main():
    
    produce=groups_produce()
    
    #print out the groups.txt
    produce.groups_produce()
    
    #print out the knockout.txt
    produce.knockout_produce()
    
    #print out the ages.txt
    produce.ages_produce()
    
    #print out the histogram.txt
    produce.histogram_produce()
    
    #print out the scorer.txt
    produce.scorer_produce()
    
    #print out the yellow.txt
    produce.yellow_produce()
    
if __name__ == "__main__":
    main()