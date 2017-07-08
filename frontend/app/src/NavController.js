function NavController($mdSidenav) {
  var self = this;
  var userInfo;
  $.get("/api/user", function(data, status){
    alert("Data: " + data + "\nStatus: " + status);
  });
  self.bodyText = "You're on the monitor screen"
  self.navMonitor = function(){
  	self.bodyText = "You're on the monitor screen"
  }
  self.navManagement = function(){
  	self.bodyText = "You're on the management screen"
  }
  self.navSettings = function(){
  	self.bodyText = "You're on the account settings screen"
  }
};
export default [ '$mdSidenav', NavController ];
