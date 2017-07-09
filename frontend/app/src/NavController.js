function NavController($mdSidenav) {
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
};
export default [ '$mdSidenav', NavController ];
