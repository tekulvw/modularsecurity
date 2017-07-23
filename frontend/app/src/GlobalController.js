function GlobalController($mdSidenav, $window, $interval, $scope) {
  var self = this;
 
  self.refreshData = function(s){
    $.ajax({
      url: "/api/user",
      success: function(data, status){
          self.userInfo = data;
          self.availableSystems = self.userInfo.owned_systems.concat(
                                  self.userInfo.secondary_systems);
          self.selectSystem(self.availableSystems[0]);
        },
      error: function(){
          $window.location.href = "/"
        },
      async: false
    });
  }

  self.refreshSecondaries = function(s){
    self.secondaries = s;
    $scope.$apply();
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
    $.ajax({
      url: "/api/secondary/" + s.id,
      success: function(data, status){
          self.secondaries = data;
        }
    });
    self.updateTabs();
  }

  self.selectSystemAndApply= function(s){
    self.userInfo.owned_systems[0] = s;
    self.selectSystem(s);
    $scope.$apply();
  }

  self.isOwner = function(){
    return $.inArray(self.currentSystem, self.userInfo.owned_systems) != -1
  }

  self.updateTabs = function(){
    if(self.isOwner()){
      self.tabs = [{i: 0, name: 'Monitor', url: 'partials/monitor.html'},
                  {i: 1, name: 'Management', url: 'partials/management.html'},
                  {i: 2, name: 'Account Settings', url: 'partials/settings.html'}];
      if(!self.currentTab){
        self.currentTab = self.tabs[0];
      }
      else{
        self.currentTab = self.tabs[self.currentTab.i];
      }
    }
    else{
      self.tabs = [{i: 0, name: 'Monitor', url: 'partials/monitor.html'},
                  {i: 1, name: 'Account Settings', url: 'partials/settings.html'}];
      if(!self.currentTab || self.currentTab.i != 2){
        self.currentTab = self.tabs[0];
      }
      else{
        self.currentTab = self.tabs[1];
      }
    }
  }

  self.refreshData();
  //$interval(self.refreshData, 1000)
}

export default [ '$mdSidenav', '$window', '$interval', '$scope', GlobalController ];
