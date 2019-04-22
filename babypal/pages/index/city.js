var city = require('../../utils/city.js');

//获取应用实例
const app = getApp()

Page({
  data: {
    //选中的城市
    chooseCity: '--',
    //定义字母
    letter: [],
    //定义每一个字母的高度
    letterHeight: 0,
    //窗口高度
    windowHeight: 0,
    //城市数据
    cityList: [],
    //历史选择城市
    cityHistory: [],
    showLetter: 'A',
  },
  onLoad: function() {
    //获取屏幕高度
    var windowHeight = wx.getSystemInfoSync().windowHeight;
    //console.log(wx.getSystemInfoSync().windowHeight); //504
    //console.log(wx.getSystemInfoSync().screenHeight); //568  
    var t = city.city[0].tag;
    //定义字母导航栏
    var letters = [];
    for (var i = 0; i < city.city.length; i++) {
      if (city.city[i].tag != "*热门城市") {
        letters.push(city.city[i].tag);
      }
    }
    var itemHeight = Math.floor((windowHeight - 50) / letters.length);

    // 获取历史访问过得城市    
    var cityHistory = wx.getStorageSync("cityHistory");

    this.setData({
      letter: letters,
      letterHeight: itemHeight,
      windowHeight: windowHeight,
      cityList: city.city,
      chooseCity: cityHistory[0] || '--',
      cityHistory: cityHistory,
    });
  },
  updateChooseCity: function(e) {
    //console.log(e);
    var city = e.target.dataset.city;
    console.log(city);
    var me = this;

    var cityHistory = wx.getStorageSync("cityHistory") || [];
    //如果历史访问中出现重复的城市则不添加
    if (!isInArray(cityHistory, city)) {
      cityHistory.unshift(city);
      cityHistory = cityHistory.slice(0, 6);
    }

    wx.setStorage({
      key: 'cityHistory',
      data: cityHistory,
    })

    wx.setStorage({
      key: 'selectedCity',
      data: city,
    })

    me.setData({
      chooseCity: city,
      cityHistory: cityHistory,
    });

    //设置全局变量--返回/index/index时调用
    wx.navigateBack({
      delta: 1,
    });

  },
  changeShowLetter: function(e) {
    //console.log(e)
    var showLetter = e.target.dataset.letter;
    this.setData({
      showLetter: showLetter,
    });
  },
  letterTouchMove: function(e) {
    // console.log(e)
    var pageY = e.touches[0].pageY - 50;
    var letterHeight = this.data.letterHeight;
    var index = Math.floor(pageY / letterHeight);
    var letter = this.data.letter[index];
    if (letter && letter != this.data.showLetter) {
      this.setData({
        showLetter: letter
      });
    }
  },
});

//验证数组中是否存在指定值
function isInArray(arr, val) {
  var i, iLen;
  if (!(arr instanceof Array) || arr.length === 0) {
    return false;
  }
  if (typeof Array.prototype.indexOf === 'function') {
    return !!~arr.indexOf(val)
  }
  for (i = 0, iLen = arr.length; i < iLen; i++) {
    if (val === arr[i]) {
      return true;
    }
  }
  return false;
}