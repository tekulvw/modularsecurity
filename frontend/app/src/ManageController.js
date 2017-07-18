function ManageController($mdDialog, $timeout) {
  var self = this;
  self.submitSettings = function(system){
	  $.ajax({
	  	  url: "/api/system/" + system.id,
	  	  type: "PUT",
	  	  success: function(data){
	        self.userInfo = data;
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
	  	  success: function(data){},
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
	  	  	refresh(data);
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
	  	  }
	  });
  };
};
export default [ '$mdDialog', '$timeout', ManageController ];
