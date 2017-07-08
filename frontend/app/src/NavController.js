function NavController($mdSidenav) {
  var self = this;
 
  $.ajax({
    url: "/api/user",
    success: function(data, status){
        self.userInfo = data;
      },
    async: false
  });

  self.getUserName = function(){
    return self.userInfo.fname.toUpperCase() + " FUCKING " + self.userInfo.lname.toUpperCase();
  };

  self.bodyText = "You're on the monitor screen"
  self.navMonitor = function(){
  	self.bodyText = "You're on the monitor screen"
  };
  self.navManagement = function(){
  	self.bodyText = "You're on the management screen"
  };
  self.navSettings = function(){
  	self.bodyText = "You're on the account settings screen"
  };
};
export default [ '$mdSidenav', NavController ];
