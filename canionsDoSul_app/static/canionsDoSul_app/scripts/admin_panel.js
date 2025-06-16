// document.addEventListener("DOMContentLoaded", () => {
//   const menuItems = document.querySelectorAll(".menu li");
//   const content = document.getElementById("admin-content");

//   const views = {
//     "cadastrar-taxonomia": `
//       <h2>Cadastrar Taxonomia</h2>
//       <p>Formulário de cadastro aqui...</p>
//     `,
//     "promover-usuario": `
//       <h2>Promover Usuário</h2>
//       <p>Selecione um usuário para promover.</p>
//     `,
//     "observacoes-pendentes": `
//       <h2>Observações Pendentes</h2>
//       <p>Lista de observações aguardando aprovação.</p>
//     `
//   };

//   menuItems.forEach(item => {
//     item.addEventListener("click", () => {
//       const section = item.dataset.section;
//       content.innerHTML = views[section] || "<p>Conteúdo não encontrado.</p>";
//     });
//   });
// });