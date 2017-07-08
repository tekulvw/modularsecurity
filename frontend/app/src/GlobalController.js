function GlobalController($mdSidenav) {
  var self = this;
  self.killSwitch = false;
  self.currentSystem = "System 1";
  self.availableSystems = ["System 1","System 2"];

  var originatorEv;

  self.openSystemMenu = function($mdMenu, ev){
	originatorEv = ev;
    $mdMenu.open(ev);
  };
  self.selectSystem = function(s){
  	self.currentSystem = s;
  }
}

export default [ '$mdSidenav', GlobalController ];
