function GlobalController($mdSidenav, $window) {
  var self = this;
 
  $.ajax({
    url: "/api/user",
    success: function(data, status){
        self.userInfo = data;
      },
    async: false
  });

  self.tabs = [{i: 0, name: 'Monitor', url: 'partials/monitor.html'},
              {i: 1, name: 'Management', url: 'partials/management.html'},
              {i: 2, name: 'Account Settings', url: 'partials/settings.html'}];

  self.currentTab = self.tabs[0];

  self.navToTab = function(i){
    self.currentTab = self.tabs[i];
  }
  
  self.killSwitch = false;
  self.currentSystem = "System 1";
  self.availableSystems = ["System 1","System 2"];

  var originatorEv;

  self.openMenu = function($mdMenu, ev){
	  originatorEv = ev;
    $mdMenu.open(ev);
  };
  self.selectSystem = function(s){
  	self.currentSystem = s;
  }
}

export default [ '$mdSidenav', '$window', GlobalController ];
