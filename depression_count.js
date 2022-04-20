// look through the json at "G:/xyloid/dev/Data/tiktok/tiktok-2020_07-10/tiktok-sample.json" and count the number of times the hashtag depression is used

const path = "G:/xyloid/dev/Data/tiktok/tiktok-2020_07-10/tiktok-sample.json"

// read the file
const fs = require('fs')
const data = fs.readFileSync(path, 'utf8')
const json = JSON.parse(data)

const cleanData = json.map(item => {
  return {
    infoItem: item.textExtra,
  }
})

const count = cleanData.map(item => {
  return item.infoItem.map(item => {
    return item.hashtagName === 'depression'
  }).filter(item => item === true).length
})

console.log(count)