function MonitorController() {
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
  		//toasty
  	}
  }
};
export default [ MonitorController ];
