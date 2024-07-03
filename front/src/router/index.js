import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../components/SignIn.vue';
import CreateMatch from '../components/CreateMatch.vue';
import MatchList from '../components/MatchList.vue';

const routes = [
    { path: '/', component: SignIn },
    { path: '/create-match', component: CreateMatch },
    { path: '/matches', component: MatchList }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
