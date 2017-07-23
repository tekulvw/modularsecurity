function ManageController($mdDialog, $timeout, $mdToast) {
  var self = this;
  self.submitSettings = function(system){
	  $.ajax({
	  	  url: "/api/system/" + system.id,
	  	  type: "PUT",
	  	  success: function(data){
	        self.userInfo = data;
	  	  	var toast = $mdToast.simple()
		      .textContent('System settings updated.')
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
		      .textContent('Failed to save system settings.')
		      .action('CLOSE')
		      .highlightAction(true)
		      .position("top right")
		      .hideDelay(3000);

		    $mdToast.show(toast).then(function(response) {
		      $mdToast.hide();
		  	});
	  	  },
	      data: JSON.stringify({'name': system.name,
	  							'grace_period': system.grace_period}),
	      dataType: 'json',
	      contentType: 'application/json'
	  });
  }
  
  self.addDevice = function(ev, system, refresh) {
    var confirm = $mdDialog.prompt()
      .title('Enter Device Serial Number')
      .placeholder('Serial Number')
      .targetEvent(ev)
      .ok('Enter')
      .cancel('Cancel');

    $mdDialog.show(confirm).then(function(result) {
      $.ajax({
	  	  url: "/api/device/" + result,
	  	  type: "PUT",
	  	  success: function(data){
	  	  	refresh(data);
	  	  	var toast = $mdToast.simple()
		      .textContent('Device added.')
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
		      .textContent('Failed to add device. Is the serial number correct and available?')
		      .action('CLOSE')
		      .highlightAction(true)
		      .position("top right")
		      .hideDelay(3000);

		    $mdToast.show(toast).then(function(response) {
		      $mdToast.hide();
		  	});
	  	  },
	      data: JSON.stringify({'system_id': system.id}),
	      dataType: 'json',
	      contentType: 'application/json'
	  });
    }, function() {
    });
  };

  self.saveDevice = function(ev, device){
  	$.ajax({
	  	  url: "/api/device/" + device.serial_num,
	  	  type: "PUT",
	  	  success: function(data){
	  	  	var toast = $mdToast.simple()
		      .textContent('Device saved')
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
		      .textContent('Failed to save device.')
		      .action('CLOSE')
		      .highlightAction(true)
		      .position("top right")
		      .hideDelay(3000);

		    $mdToast.show(toast).then(function(response) {
		      $mdToast.hide();
		  	});
	  	  },
	      data: JSON.stringify({'name': device.name,
	  							'enabled': device.enabled}),
	      dataType: 'json',
	      contentType: 'application/json'
	  });
  }

  self.deleteDevice = function(ev, device, refresh){
  	$.ajax({
	  	  url: "/api/device/" + device.serial_num,
	  	  type: "PUT",
	  	  success: function(data){
	  	  	refresh(data);
	  	  	var toast = $mdToast.simple()
		      .textContent('Device removed.')
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
		      .textContent('Failed to remove device.')
		      .action('CLOSE')
		      .highlightAction(true)
		      .position("top right")
		      .hideDelay(3000);

		    $mdToast.show(toast).then(function(response) {
		      $mdToast.hide();
		  	});
	  	  },
	      data: JSON.stringify({'system_id': null}),
	      dataType: 'json',
	      contentType: 'application/json'
	  });
  }

  self.addSecondary = function(ev, system, refresh) {
    var confirm = $mdDialog.prompt()
      .title('Enter Email Address To Add')
      .placeholder('email@host.tld')
      .targetEvent(ev)
      .ok('Enter')
      .cancel('Cancel');

    $mdDialog.show(confirm).then(function(result) {
      $.ajax({
	  	  url: "/api/secondary",
	  	  type: "POST",
	  	  success: function(data){
	  	  	var toast = $mdToast.simple()
		      .textContent('Secondary user added.')
		      .action('CLOSE')
		      .highlightAction(true)
		      .position("top right")
		      .hideDelay(3000);

		    $mdToast.show(toast).then(function(response) {
		      $mdToast.hide();
		  	});
	  	  	refresh(data);
	  	  },
	  	  error: function(){
	  	  	var toast = $mdToast.simple()
		      .textContent('Failed to add secondary user, make sure the user has logged in before adding them.')
		      .action('CLOSE')
		      .highlightAction(true)
		      .position("top right")
		      .hideDelay(3000);

		    $mdToast.show(toast).then(function(response) {
		      $mdToast.hide();
		  	});
	  	  },
	      data: JSON.stringify({'system_id': system.id,
	  							'user_email': result}),
	      dataType: 'json',
	      contentType: 'application/json'
	  });
    }, function() {
    });
  };

  self.removeSecondary = function(ev, key, refresh) {
    $.ajax({
	  	  url: "/api/secondary/" + key,
	  	  type: "DELETE",
	  	  success: function(data){
	  	  	refresh(data);
	  	  	var toast = $mdToast.simple()
		      .textContent('Secondary user removed.')
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
		      .textContent('Failed to remove secondary user.')
		      .action('CLOSE')
		      .highlightAction(true)
		      .position("top right")
		      .hideDelay(3000);

		    $mdToast.show(toast).then(function(response) {
		      $mdToast.hide();
		  	});
	  	  }
	  });
  };
};
export default [ '$mdDialog', '$timeout', '$mdToast', ManageController ];
