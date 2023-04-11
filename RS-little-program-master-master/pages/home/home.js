// pages/Home/home/home.js

const app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    StatusBar: app.globalData.StatusBar,
    CustomBar: app.globalData.CustomBar,
    swiperList: [{
      id: 0,
      type: 'image',
      url: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.9CF2g9vcpCsCy3kDvkJE2gHaEL?w=272&h=180&c=7&r=0&o=5&dpr=1.79&pid=1.7'
    }, {
      id: 1,
      type: 'image',
        url: 'https://tse4-mm.cn.bing.net/th/id/OIP-C.X165I5P1CyvHORoF9JyKXwHaE8?w=265&h=180&c=7&r=0&o=5&dpr=1.79&pid=1.7',
    }],
    elements: [
      {
        title: '使用说明',
        name: 'introduce',
        color: 'purple',
        icon: 'searchlist',
        url:"/pages/introduce/introduce"
  
      },
      {
        title: '学知识点',
        name: 'Learn',
        color: 'yellow',
        icon: 'wenzi',
        url: "/pages/learn/learn"
      },
      {
      title: '智能题库',
      name: 'Adaptive',
      color: 'green',
      icon: 'hotfill',
      url:"/pages/lib/libs/libs"
    },
    {
      title: '即将上线 ',
      name: 'coming',
      color: 'mauve',
      icon: 'discover'
    }]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },
  previewImage: function (e) {
    var current = e.target.dataset.src;
    wx.previewImage({
      current: current, // 当前显示图片的http链接  
      urls: this.data.cooperation_img // 需要预览的图片http链接列表  
    })
  },


  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})