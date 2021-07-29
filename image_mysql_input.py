import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
import base64
from io import BytesIO

engine = create_engine('mysql+pymysql://root:1019@localhost/image_practice', echo = False)
buffer = BytesIO()
im = Image.open('aa.jpeg')

im.save(buffer, format='jpeg')
img_str = base64.b64encode(buffer.getvalue())
print(img_str)

img_df = pd.DataFrame({'imageCode':[img_str]})
img_df.to_sql('Image', con=engine, if_exists='append', index=False)