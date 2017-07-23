function SettingsController($mdDialog, $window, $mdToast) {
  var self = this;
  self.submitSettings = function(info){
	  $.ajax({
	  	  url: "/api/user/",
	  	  type: "PUT",
	  	  success: function(data){
	        self.userInfo = data;
	      	var toast = $mdToast.simple()
		      .textContent('Settings updated successfully.')
		      .action('CLOSE')
		      .highlightAction(true)
		      .position("top right")
		      .hideDelay(3000);

		    $mdToast.show(toast).then(function(response) {
		      $mdToast.hide();
		  	});
	      },
	      error: function(){
	      	var toast = $mdToast.simple()
		      .textContent('Failed to save account settings.')
		      .action('CLOSE')
		      .highlightAction(true)
		      .position("top right")
		      .hideDelay(3000);

		    $mdToast.show(toast).then(function(response) {
		      $mdToast.hide();
		  	});
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
export default [ '$mdDialog', '$window', '$mdToast', SettingsController ];
