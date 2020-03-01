from bs4 import BeautifulSoup
import requests
import pandas as pd


url = 'https://www.imdb.com/chart/toptv/?ref_=nv_mv_250'
# url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

result = requests.get(url)
c = result.content

soup = BeautifulSoup(c, 'lxml')

summary = soup.find('div', {'class' : 'article'})


judulFilm = []
tahunFilm = []
skorFilm_imdb = []
durasiFilm = []
jumlahPengguna_imdb = []
kategoriFilm = []
deskripsiFilm = []
pemeranFilm = []
linkFilm = []



counter = 0
for row in soup.find('table').findAll('tr'):
  
  #mengambil data tahun film
  for i in row.findAll('span', {'class' : 'secondaryInfo'}):
    tahunFilm.append(i.text[1:-1])

  #mengambil nama aktor
  for i in row.findAll('td', {'class' : 'titleColumn'}):
    pemeranFilm.append(i.a['title'])

  #mengambil rating film
  for i in row.findAll('strong'):
    skorFilm_imdb.append(i.text)
    
  #mengambil judul film, link, deskripsi, kategori, durasi film, dan jumlah pengguna
  for i in row.findAll('td', {'class' : 'titleColumn'}):

    for j in i.findAll('a', href=True):

      #mengambil judul
      judulFilm.append(j.text)

      #mengambil link
      linkFilm.append('https://www.imdb.com/'+j['href'])

      #arter
      raw = requests.get('https://www.imdb.com/'+j['href']).content
      sourceCode = BeautifulSoup(raw, 'lxml')

      #mengambil deskripsi
      deskripsi = sourceCode.find('div', {'class' : 'summary_text'})
      deskripsiFilm.append(deskripsi.text.strip())

      #mengambil kategori
      data = sourceCode.find('div', {'class' : 'subtext'})
      kategoriList = data.findAll('a')

      temp = ''
      for k in range(0,len(kategoriList) - 1):
        # print(kategoriList[k].text)
         temp += kategoriList[k].text+ ', '
      kategoriFilm.append(temp[:-2])

      ##mengambil durasi
      try:
        data = sourceCode.find('time')
        durasiFilm.append(data.text.strip())
        # print(data.text[25:-21])
      except:
        durasiFilm.append('-')

      #mengambil jumlah pengguna yang memberikan rating
      ratingList = sourceCode.find('span', {'class' : 'small'})
      jumlahPengguna_imdb.append(ratingList.text)


  
  counter += 1

  # if counter == 11:
  #   break


# print(pemeranFilm)

#mengambil deskripsi film #ini cuma test
def ambilDeskripsi(url):

  raw = requests.get(url).content

  #mengambil deskripsi
  sourceCode = BeautifulSoup(raw, 'lxml')


# ambilDeskripsi('https://www.imdb.com/title/tt0988818/')
# ambilDeskripsi('https://www.imdb.com/title/tt0903747/')

# for i in range(5-1):
#   print('Judul :', judulFilm[i])
#   print('Tahun :', tahunFilm[i])
#   print('Kategori :',kategoriFilm[i])
#   print('Skor :',skorFilm_imdb[i],'dari',jumlahPengguna_imdb[i],'pengguna')
#   print('Durasi :',durasiFilm[i])
#   print('Deskripsi :',deskripsiFilm[i])
#   print('Pemeran :',pemeranFilm[i])
#   print('='*50)


#menyimpan semua data yang didapatkan kedalam file dengan format csv
dict = {'Judul' : judulFilm, 'Tahun' : tahunFilm, 'Durasi' : durasiFilm, 'Kategori' : kategoriFilm, 'Skor' : skorFilm_imdb, 'Pengguna ' : jumlahPengguna_imdb, 'Deskripsi' : deskripsiFilm, 'Pemeran' : pemeranFilm }
arter = pd.DataFrame(dict)

arter.to_csv('arter.csv', index=False)