import textwrap
import sqlite3
import os

from sqlite3 import Error
from PIL import Image, ImageDraw, ImageFont

def generate_meme(image_path, font_path, top_text, bottom_text='',
                font_size=8,stroke_width=2, name=None, savePath=None): #6
    # load image
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)
    image_width, image_height = im.size

    # load font
    font = ImageFont.truetype(font=font_path, size=int(image_height * font_size) // 100)
    
    # convert text to uppercase
    top_text = top_text.upper()
    bottom_text = bottom_text.upper()

    # text wrapping
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

    # draw top lines
    y = 10
    for line in top_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), text=line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
        y += line_height
    
    # draw bottom lines
    y = image_height - char_height * len(bottom_lines) - 15
    for line in bottom_lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        draw.text((x, y), line, fill='white', font=font, stroke_width=stroke_width, stroke_fill='black')
        y += line_height

    # save meme
    dirMeme = os.path.dirname(os.path.realpath(__file__)) + '/generatedMeme/'
    if not os.path.exists(dirMeme):
        os.makedirs(dirMeme)

    im.save(dirMeme + '/' + name + ".png")  
    
    return


class DB:
    
    def __init__(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            self.__conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)


    def select_all_memes(self,meme):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM tasks")

        rows = cur.fetchall()

        for row in rows:
            print(row)


    def select_meme_by_id(self, id):
        """
        Query tasks by priority
        :param conn: the Connection object
        :param priority:
        :return:
        """
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM meme WHERE id=?", (id,))
        rows = cur.fetchall()
        return rows


    def select_meme_not_created(self):
        """
        Query tasks by priority
        :param conn: the Connection object
        :param priority:
        :return:
        """
        cur = self.__conn.cursor()
        cur.execute("SELECT * FROM meme WHERE is_created=0")
        rows = cur.fetchall()
        return rows

if __name__ == '__main__':
    scriptDir = os.path.dirname(os.path.realpath(__file__))
    databasePath = scriptDir  + '/' + 'meme.catLook.db'
    imagePath = scriptDir  + '/' + 'template.meme.catLook.1280x720.0.png'
    fontPath = scriptDir  + '/' + 'times-new-roman-cyr-bold.ttf'
    
    conn = DB(databasePath)
    rows = conn.select_meme_not_created()

    for row in rows:
        currentName = str(row[0])+"."+row[1]+"."+row[2]+"."+row[3].replace(",", " ").replace(".", " ")
        currentTextTop = row[1]+", "+row[2]
        currentTextBottom = row[3]
        print(currentName)
        generate_meme(image_path=imagePath, font_path=fontPath, name=currentName, top_text=currentTextTop, bottom_text=currentTextBottom)
        
        #if (row[0] >= 24):break