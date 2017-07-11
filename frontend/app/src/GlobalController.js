function GlobalController($mdSidenav, $window) {
  var self = this;
 
  $.ajax({
    url: "/api/user",
    success: function(data, status){
        self.userInfo = data;
      },
    error: function(){
        $window.location.href = "/"
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
  self.availableSystems = self.userInfo.owned_systems.concat(
                            self.userInfo.secondary_systems);
  
  self.currentSystem = self.availableSystems[0];

  var originatorEv;

  self.openMenu = function($mdMenu, ev){
	  originatorEv = ev;
    $mdMenu.open(ev);
  };

  self.selectSystem = function(s){
  	self.currentSystem = s;
    self.updateTabs();
    console.log(s);
  }

  self.updateTabs = function(){
    if($.inArray(self.currentSystem, self.userInfo.owned_systems) != -1){
      self.tabs = [{i: 0, name: 'Monitor', url: 'partials/monitor.html'},
                  {i: 1, name: 'Management', url: 'partials/management.html'},
                  {i: 2, name: 'Account Settings', url: 'partials/settings.html'}];
    }
    else{
      self.tabs = [{i: 0, name: 'Monitor', url: 'partials/monitor.html'},
                  {i: 2, name: 'Account Settings', url: 'partials/settings.html'}];
    }
  }
}

export default [ '$mdSidenav', '$window', GlobalController ];
