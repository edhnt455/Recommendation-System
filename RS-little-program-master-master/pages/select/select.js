var app = getApp()
Page({
    data: {
      array: ['摸底测试', '推荐界面','考试界面'],
      objectArray: [
        {
          id: 0,
          name: '摸底测试'
        },
        {
          id: 1,
          name: '推荐界面'
        },
        {
          id: 2,
          name: '考试界面'
        }
      ]
    },
    bindPickerChange: function (e) {
      console.log('picker发送选择改变，携带值为', e.detail.value)
      this.setData({
        index: e.detail.value
      })
      if(this.data.index == 1){
        wx.request({
          url: 'http://127.0.0.1:5000/user/recommend_exam',
          method: "POST",
          data: {  
            username: app.globalData.username
          }, 
          success: function(res)
          {  
            // console.log(res.data); 
            if(res.data.code==400)
            { 
              wx.showToast({
                title: '返回错误',
                icon: 'none',
                duration: 2000  //持续的时间
              })  
            } 
            else
            {     // 调用globaldata
              app.globalData.questionList = res.data; 
              console.log(app.globalData.questionList)
              wx.navigateTo({
                url: '/pages/recommend/recommend'
                })
            }
          }
        })
      }
      else if(this.data.index == 2)
      {
        wx.request({
          url: 'http://127.0.0.1:5000/user/final_exam',
          method: "POST",
          // data: {  
          //   username: that.data.username,
          //   password: that.data.password
          // }, 
          success: function(res)
          { 
            // console.log(res.data); 
            if(res.data.code==400)
            { 
              wx.showToast({
                title: '返回错误',
                icon: 'none',
                duration: 2000  //持续的时间
              })  
            }
            else      
            {     // 调用globaldata
              app.globalData.questionList = res.data; 
              console.log(app.globalData.questionList)
              wx.navigateTo({
                url: '/pages/finalexam/finalexam'
                })
            }
          }
        })
      }
      else{
        wx.request({
          url: 'http://127.0.0.1:5000/user/exam',
          method: "POST",
          // data: {  
          //   username: that.data.username,
          //   password: that.data.password
          // }, 
          success: function(res)
          { 
            // console.log(res.data); 
            if(res.data.code==400)
            { 
              wx.showToast({
                title: '错误',
                icon: 'none',
                duration: 2000  //持续的时间
              })
            }  
            else
            {     // 调用globaldata
              app.globalData.questionList = res.data; 
              console.log(app.globalData.questionList)
              wx.navigateTo({
                url: '/pages/exam/exam'
                })
            }
          }
        })
      }
    }
  })
