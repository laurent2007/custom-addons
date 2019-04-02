//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    imgUrls: [
      '/images/swiper01s.jpg',
      '/images/swiper02s.jpg',
      '/images/swiper03s.jpg'
    ],
    indicatorDots: true,
    autoplay: true,
    interval: 5000,
    duration: 1000,

    navlist:[
      {
        nav_src:'/images/icon.png',
        nav_title:'新人专享'
      },
      {
        nav_src: '/images/icon.png',
        nav_title: '每日抽奖'
      },
      {
        nav_src: '/images/icon.png',
        nav_title: '0元拿'
      },
      {
        nav_src: '/images/icon.png',
        nav_title: '添加有礼'
      }
    ],

    proList: [
      {
        logo: "/images/1.jpg",
        title: "飞羽宝宝早教中心",
        desc: "四川山水甲天下\n有山有水好风光",
        label:'本地区最热推荐',
        province:'   闵行区',
        tag:'0-12岁 小课时包',
        type:'儿童美术',
        price:'4770',
        distance:'500'
      },
      {
        logo: "/images/2.jpg",
        title: "葡萄云美术教育",
        desc: "地中海传奇\n一生一定要去的地方",
        label: '本地区最热推荐',
        province: '   闵行区',
        tag: '0-12岁 小课时包',
        type: '艺术启蒙',
        price: '4770',
        distance: '500'
      },
      {
        logo: "/images/3.jpg",
        title: "蒙特利梭国际早教中心",
        desc: "印度泰姬陵\n看阿三看阿三",
        label: '本地区最热推荐',
        province: '   闵行区',
        tag: '0-12岁 小课时包',
        type: '蒙氏教育',
        price: '4770',
        distance: '500'
      }
    ],

  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
