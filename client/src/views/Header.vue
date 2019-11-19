<template>
<div>
    <b-button @click="toggleBusy">Toggle Busy State</b-button>

    <b-table  :items="items" :busy="isBusy" :fields="fields" primary-key="ID" class="mt-3" outlined striped small >
      <template v-slot:table-busy>
        <div class="text-center text-danger my-2">
          <b-progress :value="value" :max="max" show-progress animated></b-progress>
        </div>
      </template>
    </b-table>
    <div > 
        <br><br>
       <b-container>
           <b-row>
               <b-col>
                    <li v-for="item in items" :key="item">
                        <b-card bg-variant="dark" text-variant="white" header="Primary" class="text-center">
                        <b-card-text>{{item.ID}}</b-card-text>
                        </b-card>
                        <br>
                    </li>   
               </b-col>
               <b-col>
                    <li v-for="item in items" :key="item">
                        <b-card bg-variant="dark" text-variant="white" header="Primary" class="text-center">
                        <b-card-text>{{item.machine}}</b-card-text>
                        </b-card>
                        <br>
                    </li>
               </b-col>
               <b-col>
                    <li v-for="item in items" :key="item">
                        <b-card bg-variant="dark" text-variant="white" header="Primary" class="text-center">
                        <b-card-text>{{item.STATUS}}</b-card-text>
                        </b-card>
                        <br>
                    </li>
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
        
            value: 0,
            max: 100,
            isBusy: false,
            fields: [
                {
                    key: 'ID',
                    sortable: true
                },
                {
                    key: 'machine',
                    sortable: true,
                },
                {
                    key: 'RAM',
                    sortable: true
                },
                {
                    key: 'CPU',
                    sortable: true
                },
                {
                    key: 'STATUS',
                    sortable: true
                }
            
            ],
            items: [
                { ID: 1, machine: 'Desktop', CPU: 0.9, RAM: 2.0 ,STATUS: "Active"},
                { ID: 2, machine: 'Desktop', CPU: 0.5, RAM: 2.4 ,STATUS: "Active" },
                { ID: 3, machine: 'Mobile', CPU: 0.2, RAM: 1.2 ,STATUS: "Deactive"},
                { ID: 4, machine: 'Mobile', CPU: 0.3, RAM: 3.0 ,STATUS: "Active"}
            ],
            item: []
        }
    },
  methods: {
        toggleBusy() {
        this.isBusy = !this.isBusy
        this.value =0
        for (var i =0 ;i<100;i++){
            this.value++
        }
      }
  }
}

</script>