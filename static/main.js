$(document).ready(() => {
    console.log("ready!");
    
    // Intercept on form submission 
    $('form').on('submit', () => {
      
      let oldAudio = 'test'

      // Retrieve input values
      phrase = $('input[name="phrase"]').val();
  
      $.ajax({
        type: "POST",
        url: "/",
        data : { 'phrase': phrase, 'oldAudio': oldAudio },
        success: (results) => {

          if (results.score < 50){
            $('#results').html('NOT SARCASTIC! ' + 'I feel that this has a ' + results.score + '% chance of being sarcastic...')
            //$('#results').html('Hmm, just about ' + results.score + '% chance of being Sarcastic!')
          } else {
            $('#results').html('SARCASTIC! ' + 'My mind tells me this has a  ' + results.score + '% chance of being sarcastic!')
          }
          
          // Load new audio
          $("#player").attr('src', results.newAudio);
          oldAudio = results.oldAudio

          // Box Animator
          function loop(rectGrow, rectShrink, growAmt, shrinkAmt) {
            $(rectGrow).css({width:200,height:75});
            $(rectShrink).css({width:200,height:75});
            
            $(rectGrow).animate ({
                width: growAmt
            }, 500, 'linear', function() {});
            
            $(rectShrink).animate ({
              width: shrinkAmt
            }, 500, 'linear', function() {});
          }

          // Calculate loop params based on sarcastic score
          let amt = results.score-50;
          let add = '+=' + amt/100*200*2;
          let subtract = '-=' + amt/100*200*2;
          if(results.score > 50){
            loop('#rect2', '#rect1', add, subtract);
          }
          else{
            loop('#rect1', '#rect2', subtract, add);
          }

        },
        error: (error) => {
          console.log(error)
        }
      });
  
    });
  
  });