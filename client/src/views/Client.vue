<template>
<div class="bg-dark text-white">

    

    <span class="font-weight-bold  text-lg-left">Check Text:</span>

    <b-container class="bv-example-row ">
    <b-row>   
        <b-form-textarea 
            id="textareaa"
            v-model="text"
            placeholder="Type type something"
            rows="6"
            max-rows="12"
            :disabled="loading">
        </b-form-textarea>
         
    </b-row>
    <br> <br>
    <b-row>
        <b-col>
             <b-button size="lg" variant="outline-light" v-on:click="send"> Submit</b-button> 
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

            <div v-show="loading">
                <b-spinner big ></b-spinner> 
                <p>Sending</p> 
                
            </div>


            </b-col>
        </b-row>
    </b-container>
   </div>

   <div v-if="errors != null" class="bg-white text-white">
    <b-container class="bg-red text-white">
        <b-row>
            <b-col>
                <h3> {{ errors.length }} errors found:</h3>
                <p>
                    <span v-for="word in showText.split(' ')" :key=word :class="errors.indexOf(word) >= 0 ? 'text-danger' : 'text-dark'">{{ word }} </span>
                </p>
            </b-col>
        </b-row>
    </b-container>
   </div>

</div>
</template>

<script>
import Axios from 'axios'

export default {
    data() {
        return {
            text: '',
            loading : false,
            showText: '',
            errors: null,
        }
    },
  methods: {
    send: function () {
        this.visibility()
        Axios.get('http://localhost:8000/spellcheck?text=' + this.text, ).then(response => {
            console.log(response)
            this.showText = this.text
            this.showErrors(response.data.wrong_words);
        })
    },
    visibility: function () {
        this.loading = true;
    },
    showErrors: function(errors) {
        this.loading = false;
        
        this.errors = errors
    },
    clear: function () {
        this.text = "";
        this.loading = false;
        this.errors = null;
    }

  }
}
</script>