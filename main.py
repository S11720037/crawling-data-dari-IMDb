'''
Arter Tendean
01-03-2020

Program untuk mengambil data dari imdb dan rottentomatoes
'''


from bs4 import BeautifulSoup
from rotten_tomatoes_client import RottenTomatoesClient
import requests
import pandas as pd

#membuat list untuk menyimpan data
judulFilm = []
tahunFilm = []
skorFilm_imdb = []
durasiFilm = []
jumlahPengguna_imdb = []
kategoriFilm = []
deskripsiFilm = []
pemeranFilm = []
linkFilm = []
skorFilm_tomatoes = []
skorFilmDariPengguna_tomatoes = []
jumlahPengguna_tomatoes = []
nomor = []


#imdb
def imdb(url):
  result = requests.get(url)
  sourceCode = result.content
  soup = BeautifulSoup(sourceCode, 'lxml')
  summary = soup.find('div', {'class' : 'article'})

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

        #mengambil source code halaman
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

        #mengambil durasi
        try:
          data = sourceCode.find('time')
          durasiFilm.append(data.text.strip())
          # print(data.text[25:-21])
        except:
          durasiFilm.append('-')

        #mengambil jumlah pengguna yang memberikan rating
        ratingList = sourceCode.find('span', {'class' : 'small'})
        jumlahPengguna_imdb.append(ratingList.text)


#rottentomatoes
def tomatoes(daftarJudul):
  global nomor

  #mengambil link sesuai dengan judul film
  links = []
  for judul, index in zip(daftarJudul, range(1, len(daftarJudul) + 1)):
    
    nomor.append(index)#list untuk nomor film

    #mengambil link rottentomatoes berdasarkan judul film dengan menggunakan API
    result = RottenTomatoesClient.search(term=judul, limit=5)
    try:
      # print(i,result['tvSeries'][0]['url'])
      links.append('https://www.rottentomatoes.com' + result['tvSeries'][0]['url'])
    except:
      # print(i,'-')
      links.append('-')

  #mengambil skor, skor rata-rata, dan jumlah pengguna
  for link in links:
    try:
      data = requests.get(link)
      data = BeautifulSoup(data.content, 'lxml')
      score = data.findAll('span', {'class' : 'mop-ratings-wrap__percentage'})
      users = data.findAll('strong', {'class' : 'mop-ratings-wrap__text--small'})
      try:
        # print(score[0].text.strip())
        skorFilm_tomatoes.append(score[0].text.strip())
      except:
        # print('-')
        skorFilm_tomatoes.append('-')
      try:
        # print(score[1].text.strip())
        skorFilmDariPengguna_tomatoes.append(score[1].text.strip())
      except:
        # print('-')
        skorFilmDariPengguna_tomatoes.append('-')
      try:
        # print(users[1].text.strip())
        jumlahPengguna_tomatoes.append(users[1].text.strip()[14:])
      except:
        # print('-')
        jumlahPengguna_tomatoes.append('-')
    except:
      skorFilm_tomatoes.append('-')
      skorFilmDariPengguna_tomatoes.append('-')
      jumlahPengguna_tomatoes.append('-')
      

#memanggil fungsi untuk menjalankan program
imdb('https://www.imdb.com/chart/toptv/?ref_=nv_mv_250')
tomatoes(judulFilm)

#menyimpan semua data yang didapatkan kedalam file dengan format csv
dict = {'No' : nomor,
        'Judul' : judulFilm, 'Tahun' : tahunFilm, 'Durasi' : durasiFilm, 'Kategori' : kategoriFilm, 'Skor IMDb' : skorFilm_imdb, 'Pengguna IMDb' : jumlahPengguna_imdb, 'Deskripsi' : deskripsiFilm, 'Pemeran' : pemeranFilm,
        'Skor RottenTomatoes' : skorFilm_tomatoes, 'Skor RottenTomatoes Dari Pengguna' : skorFilmDariPengguna_tomatoes, 'Pengguna RottenTomatoes' : jumlahPengguna_tomatoes}
arter = pd.DataFrame(dict)

arter.to_csv('arter.csv', index=False)
