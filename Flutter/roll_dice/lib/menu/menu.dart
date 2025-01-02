import 'package:flutter/material.dart';
import 'package:roll_dice/menu/products.dart';
import 'package:roll_dice/menu/profile.dart';

class Menu extends StatefulWidget {
  const Menu({super.key});

  @override
  State<Menu> createState() {
    return _Menu();
  }
}

class _Menu extends State<Menu> {
  Widget produtos = Products();
  Widget perfil = Profile();
  Widget activatePage = Products();

  switchPage(Widget page) {
    setState(() {
      activatePage = page;
    });
  }

  @override
  Widget build(context) {
    return Column(children: [
      Padding(
        padding: const EdgeInsets.only(top: 20),
        child: Image.asset(
          'assets/images/deltaprice_hori.png',
          width: 400,
        ),
      ),
      Text(
        'Menu',
        style: TextStyle(fontSize: 40),
      ),
      activatePage,
      Row(children: [
        TextButton.icon(
            onPressed: switchPage(produtos),
            style: TextButton.styleFrom(
                padding: const EdgeInsets.all(20), minimumSize: Size(40, 40)),
            icon: const Icon(Icons.import_contacts_sharp),
            label: const Text('Produtos')),
        TextButton.icon(
            onPressed: switchPage(perfil),
            style: TextButton.styleFrom(
                padding: const EdgeInsets.all(20), minimumSize: Size(40, 40)),
            icon: const Icon(Icons.import_contacts_sharp),
            label: const Text('Perfil')),
      ])
    ]);
  }
}
