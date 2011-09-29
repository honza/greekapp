var _;

_ = function(func, context) {
  return(function() {
    return func.apply(context, arguments); 
  });
};
