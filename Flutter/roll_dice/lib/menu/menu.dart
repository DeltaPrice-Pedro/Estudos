import 'package:flutter/material.dart';

class Menu extends StatefulWidget {
  const Menu({super.key});

  @override
  State<Menu> createState() {
    return _Menu();
  }
}

class _Menu extends State<Menu> {
Widget activatePage = Products()

  void switchPage(Widget page) {
    setState(() {
      activatePage = page
    });
  }

  @override
  Widget build(context) {
    return Column(children: [
      Text(
        'Menu',
        style: TextStyle(fontSize: 40),
      ),
      activatePage,
      Row(children:[TextButton.icon(
          onPressed: switchPage(Products),
          style: TextButton.styleFrom(
              padding: const EdgeInsets.all(20),
              minimumSize: Size(40, 40)),
          icon: const Icon(Icons.import_contacts_sharp),
          label: const Text('Produtos')),TextButton.icon(
          onPressed: switchPage(History),
          style: TextButton.styleFrom(
              padding: const EdgeInsets.all(20),
              minimumSize: Size(40, 40)),
          icon: const Icon(Icons.import_contacts_sharp),
          label: const Text('Histórico')),
          TextButton.icon(
          onPressed: switchPage(Profile),
          style: TextButton.styleFrom(
              padding: const EdgeInsets.all(20),
              minimumSize: Size(40, 40)),
          icon: const Icon(Icons.import_contacts_sharp),
          label: const Text('Perfil')),])
      
    ]);
  }
}
