import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
import base64
from io import BytesIO

engine = create_engine('mysql+pymysql://root:1019@localhost/image_practice', echo = False)
img_df = pd.read_sql(sql='select * from Image', con=engine)
img_str = img_df['imageCode'].values[0]

img = base64.decodebytes(img_str)

im = Image.open(BytesIO(img))
im.show()