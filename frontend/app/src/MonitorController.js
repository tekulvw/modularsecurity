function MonitorController() {
  var self = this;

  self.toggleEnable = function(ev, device){
  	$.ajax({
	  	  url: "/api/device/" + device.serial_num,
	  	  type: "PUT",
	  	  success: function(data){},
	      data: JSON.stringify({'enabled': !device.enabled}),
	      dataType: 'json',
	      contentType: 'application/json'
	  });
  }
};
export default [ MonitorController ];
