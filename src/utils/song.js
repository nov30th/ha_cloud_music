import { toHttps } from './util'

function filterSinger(singers) {
  let arr = []
  singers.forEach(item => {
    arr.push(item.name)
  })
  return arr.join('/')
}

export class Song {
  constructor({ id, name, singer, album, image, duration, url, albumId }) {
    this.id = id
    this.name = name
    this.singer = singer
    this.album = album
    this.image = image
    this.duration = duration
    this.url = url
    this.albumId = albumId
  }
}

export function createAlbumList(music) {
  return new Song({
    id: music.id,
    name: music.name,
    singer: music.artists.length > 0 && filterSinger(music.artists),
    album: music.album.name,
    image: music.album.picUrl || null,
    duration: music.duration / 1000,
    url: `https://music.163.com/song/media/outer/url?id=${music.id}.mp3`,
    albumId: music.album.id
  })
}

export function createPlayList(music) {
  return new Song({
    id: music.id,
    name: music.name,
    singer: music.artists.length > 0 && filterSinger(music.artists),
    album: music.album.name,
    image: music.album.picUrl || null,
    duration: music.duration / 1000,
    url: `https://music.163.com/song/media/outer/url?id=${music.id}.mp3`,
    albumId: music.album.id
  })
}

export function createTopList(music) {
  return new Song({
    id: music.id,
    name: music.name,
    singer: music.ar.length > 0 && filterSinger(music.ar),
    album: music.al.name,
    image: music.al.picUrl,
    duration: music.dt / 1000,
    url: `https://music.163.com/song/media/outer/url?id=${music.id}.mp3`,
    albumId: music.al.id
  })
}

// 歌曲数据格式化
// const formatAlbumSongs = function formatAlbumSongs(list) {
//   let Songs = []
//   list.forEach(item => {
//     const musicData = item
//     if (musicData.id) {
//       Songs.push(createAlbumList(musicData))
//     }
//   })
//   return Songs
// }


const formatSongs = function formatPlayList(list) {
  let Songs = []
  list.forEach(item => {
    const musicData = item
    if (musicData.id) {
      Songs.push(createPlayList(musicData))
    }
  })
  return Songs
}

export const formatTopSongs = function formatTopList(list) {
  let Songs = []
  list.forEach(item => {
    const musicData = item
    if (musicData.id && musicData.al.id) {
      Songs.push(createTopList(musicData))
    }else if(musicData.id && musicData.album && musicData.album.id)
      Songs.push(createAlbumList(musicData))
  })
  return Songs
}

export default formatSongs
