<template>
<div class="bg-dark text-white">

    

    <span class="font-weight-bold  text-lg-left">Check Text:</span>

    <b-container class="bv-example-row ">
    <b-row>   
        <b-form-textarea 
            id="textareaa"
            v-model="message"
            placeholder="Type type something"
            rows="6"
            max-rows="12"
            :disabled="var_">
        </b-form-textarea>
         
    </b-row>
    <br> <br>
    <b-row>
        <b-col>
             <b-button size="lg" variant="outline-light" v-on:click="visibility"> Submit</b-button> 
        </b-col>
        <b-col> 
            <b-button size="lg" variant="outline-light" v-on:click="clear">Clear</b-button>   
        </b-col>
        
    </b-row>
    <br> <br>
    </b-container>
    
    <div class="bg-success text-white">
    <b-container class="bg-red text-white">
        <b-row>
            <b-col>

            <div v-show="var_">
                <b-spinner big ></b-spinner> 
                <p>Sent</p> 
                
            </div>


            </b-col>
        </b-row>
    </b-container>
   </div>

</div>
</template>

<script>
export default {
    data() {
        return {
            message: '',
            var_ : false
        }
    },
  methods: {
    visibility: function () {
        this.var_ = true
        
    },
    clear: function () {
    
        this.message = ""
        this.var_ = false
        
    }

  }
}
</script>