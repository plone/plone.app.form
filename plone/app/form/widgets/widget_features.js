function saveWarning(){
// Hide or show save warning message, depending of any
// search result has been selected
    jq('.ubermultiselectwidget').each(function(){
        if(jq(this).find(':checked').length){
            jq(this).find('.save_reminder').show();
        }else{
            jq(this).find('.save_reminder').hide();             
        }
    });
}

