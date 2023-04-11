// pages/register/register.js
var app = getApp()
Page({

  data: {
      username:'',
      password:'',
      password2:''
  },
  usernameInput:function(e)
  {
    this.setData({
      username: e.detail.value
    })
  },


  passwordInput:function(e)
  {
    this.setData({
      password: e.detail.value
    })
  },

  passwordInput2:function(e)
  {
    this.setData({
      password2: e.detail.value
    })
  },




  register:function()
  {
    var that = this;
    if(that.data.password==that.data.password2){
    wx.request({
      url: 'http://skyhook.cloud:5000/user/register',
      method:"POST",
      data:{
        username:that.data.username,
        password:that.data.password
      },
      success: function(res)
      {
        if(res.data.code==200)
        {
          wx.showToast({  
            title: '注册成功',
            icon: 'success',
            duration: 1000  
          })
          wx.navigateTo({
            url: "/pages/login/login"
            })
        }
        else if(res.data.code==405)
        {
            wx.showToast({
              title: '用户名已存在',
              icon: 'warn',
              duration: 10000
            })
            wx.navigateTo({
              url: "/pages/register/register"
              })
          }
      }
    })
  }
   else 
   {
     wx.showToast({
     title: '密码不一致',
     icon: 'loading',
     duration: 1000
                 })
    }

}

 





















})