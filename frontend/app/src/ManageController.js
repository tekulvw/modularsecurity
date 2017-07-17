function ManageController($mdDialog) {
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
  
  self.addDevice = function(ev, system) {
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
	  	  success: function(data){},
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

  self.deleteDevice = function(ev, device){
  	$.ajax({
	  	  url: "/api/device/" + device.serial_num,
	  	  type: "PUT",
	  	  success: function(data){},
	      data: JSON.stringify({'system_id': null}),
	      dataType: 'json',
	      contentType: 'application/json'
	  });
  }

  self.addSecondary = function(ev) {
    var confirm = $mdDialog.prompt()
      .title('Enter Email Address To Add')
      .placeholder('email@host.tld')
      .targetEvent(ev)
      .ok('Enter')
      .cancel('Cancel');

    $mdDialog.show(confirm).then(function(result) {
      console.log("User Added: "+ result);
    }, function() {
    });
  };
};
export default [ '$mdDialog', ManageController ];
