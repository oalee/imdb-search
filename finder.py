# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from imdb import find_move_by_name
from pathlib import Path
import subprocess
import logging
import os
from parse import *

logging.basicConfig(level= logging.INFO)

def currectName(name):
    name = name.lower()
    cn = ""
    qualities = ["720" , "1080" , "brip" , "bluray" , "dvd" ,"m-hd", "hd" , "web" , "brrip", "criterion"
    , "blu-ray" , "director's cut" , "bdrip" , "x264" , "hdtv" , "xvid" , "ntsc" ]
    for q in qualities:
        if name.count(q) > 0:
            cn = q
            break
    if len(cn)> 0:
        name = name.split(cn)[0]
    forbidden_list = [ "-" , ")" , "(" , "]" , "[", "{" , "}"]
    name = name.replace("." , " ").replace('_' , " ")
    doReplace = False
    temp = ""
    for j in name:
        if j == '[':
            doReplace = True

        if not doReplace and j not in forbidden_list:
            temp += j

        if j == ']':
            doReplace = False

    name = temp.split(" ")
    index = len(name)
    while index > 0:
        index = index - 1
        try:
            year = int(name[index])
            if year > 1900 :
                break
        except:
            pass
    if index > 0 :
        temp = ""
        for k in range(0,index):
            temp += name[k]
            temp += " "
    return temp

def print_to_file(file,map):
    file.write('title : ' + map['title'] + "\n")
    file.write('rating : ' + map['rating']+ "\n")
    file.write('metascore : ' + str(map['metascore'])+ "\n")
    file.write('year : ' + map['year']+ "\n")
    file.write('genre : ' + str(map['genre'])+ "\n")
    file.write('storyline : ' + map['storyline'])
    file.write('dir : ' + map['dir'] + "\n")
    file.write('size : ' + map['size']+ "\n")
    file.write('-------------------------------------\n')

def read_from_raw_file(maps , raw_file):
    i = 0
    while not raw_file.tell() == os.fstat(raw_file.fileno()).st_size :
        map = {}
        i = int(raw_file.readline())
        for i in range(0,8):
            line = raw_file.readline()
            r = parse("{} : {}" , line)
            print(r )
            print(line)
            map[str(r[0])] = str(r[1])
            if str(r[0]) == "storyline":
                map["storyline"] = raw_file.readline()
            if str(r[0]) == "metascore" and r[1] == "\n":
                map["metascore"] = 0
                raw_file.readline()
                raw_file.readline()
                raw_file.readline()

        print(map)
        maps.append(map)
        raw_file.readline()
    return i

def du(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')

def tryToFindMovie(name):
    try:
        map = find_move_by_name(name)
        return map
    except:
        print('error happend , skip this y/n ?' )
        x= "s"
        while x != "y" or x != "n" :
            x = input()
        if x == "y":
            tryToFindMovie(name)
        else :
            return


dirs = ['/run/media/al/Data III/Movies' , '/run/media/al/Data/MoviE' ,'/run/media/al/Data/MoviE/2012', '/run/media/al/Data/MoviE/2011 Movies', '/run/media/al/Data/Movies' ,
    '/run/media/al/Data II/Movies' , '/run/media/al/Data II/Movies_2' , '/run/media/al/Data II/Movies 2015' , '/run/media/al/Data IV/Movies']

movies_list = []



for dir in dirs:
    movies_list += [(str(x).split("/")[-1] , str(x) , du(str(x))) for x in Path(dir).iterdir()]

for item in movies_list:
    logging.info(item)

writer_file = open('my_movies','w')
maps = []


t = read_from_raw_file(maps , open('raw_file','r'))



for i in range(t,0):
    raw_file = open('raw_file' , 'a')
    map = tryToFindMovie(currectName(movies_list[i][0]))
    print(movies_list[i][0] , map)

    if map == None or map['title'] is "":
        logging.info("could not find movie by name " + currectName(movies_list[i][0]))
        continue
    map['size'] =  str(movies_list[i][2])
    map['dir'] = movies_list[i][1]
    if not 'rating' in map :
        map['rating'] = 0
    logging.info('got the detail of movie , map is ' + str(map))
    raw_file.write(str(i) + "\n")
    print_to_file(raw_file , map)
    raw_file.close()
    maps.append(map)

sorted_map = sorted(maps,key = lambda map : -1 * float(map['rating']+"0"))
for map in sorted_map:
    print_to_file(writer_file , map)
writer_file.close()
