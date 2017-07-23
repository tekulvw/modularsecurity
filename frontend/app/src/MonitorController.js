function MonitorController($mdToast, $scope, $interval) {
  var self = this;

  self.toggleEnable = function(ev, device, permission){
  	if(permission){
	  	$.ajax({
		  	  url: "/api/device/" + device.serial_num,
		  	  type: "PUT",
		  	  success: function(data){},
		      data: JSON.stringify({'enabled': !device.enabled}),
		      dataType: 'json',
		      contentType: 'application/json'
		  });
  	}
  	else{
	    var toast = $mdToast.simple()
		      .textContent('You do not have permission to manage this device.')
		      .action('CLOSE')
		      .highlightAction(true)
		      .position("top right")
		      .hideDelay(3000);

		    $mdToast.show(toast).then(function(response) {
		      $mdToast.hide();
		  	});
  	}
  }


	self.gottenData = false;
	self.lastSystem = null;

	self.getDataFrames = function(system){
		if(system == null){
			system = self.lastSystem;
		}
		else{
			self.lastSystem = system;
		}
		$.ajax({
	  	  url: "/api/system/" + system.id + "/dataframes",
	  	  type: "GET",
	  	  success: function(data){
	  	  	self.dataFrames = data;
	  	  	self.gottenData = true;
	  	  },
	  	  async: false
	  });
	}

	self.getDeviceData = function(device, system){
		if(!self.gottenData){
			self.getDataFrames(system);
		}
		var ret = "Loading...";
		$.ajax({
		  	  url: self.dataFrames[device.serial_num],
		  	  type: "GET",
		  	  success: function(data){
		  	  	ret = data;
		  	  },
		  	  error: function(){
			    ret ={open: "failed to get data"};
		  	  },
		  	  async: false
	  		});
		return ret;
	}

	$interval(function(){self.getDataFrames();}, 5000);

};
export default [ '$mdToast', '$scope', '$interval', MonitorController ];
