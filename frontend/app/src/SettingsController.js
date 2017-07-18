function SettingsController($mdDialog, $window) {
  var self = this;
  self.submitSettings = function(info){
	  $.ajax({
	  	  url: "/api/user/",
	  	  type: "PUT",
	  	  success: function(data){
	        self.userInfo = data;
	      },
	      data: JSON.stringify({'phone_num': info}),
	      dataType: 'json',
	      contentType: 'application/json'
	  });
  }

  self.logout = function(){
  	$.ajax({
	  	  url: "/api/logout",
	  	  success: function(data){
	  	  	$window.location.href = "/";
	      }
	  });
  }

  	
  
  self.createDevice = function(ev) {
    var confirm = $mdDialog.prompt()
      .title('Enter Device Serial Number')
      .placeholder('Serial Number')
      .targetEvent(ev)
      .ok('Enter')
      .cancel('Cancel');

    $mdDialog.show(confirm).then(function(result) {
    	$.ajax({
		    url: "/api/device",
		    type: "POST",
		    data: JSON.stringify({'serial_number': result}),
		    dataType: 'json',
		    contentType: 'application/json'
		});
    }, function() {
    });
  };
};
export default [ '$mdDialog', '$window', SettingsController ];
