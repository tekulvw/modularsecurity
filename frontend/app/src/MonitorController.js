function MonitorController($mdToast, $scope) {
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
	    $mdToast.show(
	      $mdToast.simple()
	        .textContent('Failed to update device.')
	        .position("top right")
	        .hideDelay(1500)
	    );
  	}
  }


	self.gottenData = false;

	self.getDataFrames = function(system){
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

};
export default [ '$mdToast', '$scope', MonitorController ];
