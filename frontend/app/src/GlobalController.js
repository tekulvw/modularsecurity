function GlobalController($mdSidenav, $window) {
  var self = this;
 
  self.refreshData = function(){
    $.ajax({
      url: "/api/user",
      success: function(data, status){
          self.userInfo = data;
          self.updateTabs();

          self.availableSystems = self.userInfo.owned_systems.concat(
                                  self.userInfo.secondary_systems);
          self.selectSystem(self.availableSystems[0])
        },
      error: function(){
          $window.location.href = "/"
        },
      async: false
    });
  }


  self.navToTab = function(i){
    self.currentTab = self.tabs[i];
  }

  var originatorEv;

  self.ks = function(){
    $.ajax({
        url: "/api/system/" + self.currentSystem.id + "/killswitch",
        type: "PUT",
        data: JSON.stringify({'ks_enabled': !self.currentSystem.ks_enabled}),
        dataType: 'json',
        contentType: 'application/json'
    });
  }

  self.openMenu = function($mdMenu, ev){
	  originatorEv = ev;
    $mdMenu.open(ev);
  };

  self.selectSystem = function(s){
  	self.currentSystem = s;
    self.updateTabs();
    if(!self.currentTab){
      self.currentTab = tabs[self.currentTab.i];
    }
    else{
      self.currentTab = tabs[0];
    }
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

  self.refreshData();
}

export default [ '$mdSidenav', '$window', GlobalController ];
