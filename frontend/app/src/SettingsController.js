function SettingsController() {
  var self = this;
  self.submitSettings = function(info){
	  $.ajax({
	  	  url: "/api/user",
	  	  type: "POST",
	  	  success: function(data){
	        self.userInfo = data;
	      },
	      data: JSON.stringify(info),
	      dataType: 'json'
	  });
  }
};
export default [ SettingsController ];
