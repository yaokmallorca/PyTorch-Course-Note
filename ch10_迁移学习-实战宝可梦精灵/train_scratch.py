import torch
from torch import optim, nn
from torch.utils.data import DataLoader
import visdom
from pokemon import Pokemon
from resnet import ResNet18

batch_size = 256
lr = 1e-3
epoches = 10

device = torch.device('cuda')
torch.manual_seed(1234)

train_db = Pokemon('../data/pokemon', 224, mode='train')
val_db = Pokemon('../data/pokemon', 224, mode='val')
test_db = Pokemon('../data/pokemon', 224, mode='test')
train_loader = DataLoader(train_db, batch_size=batch_size, shuffle=True, num_workers=4)
val_loader = DataLoader(val_db, batch_size=batch_size, num_workers=2)
test_loader = DataLoader(test_db, batch_size=batch_size, num_workers=2)

viz = visdom.Visdom()


def evalute(model, loader):
    correct = 0
    total = len(loader.dataset)
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        with torch.no_grad():
            logits = model(x)
            pred = logits.argmax(dim=1)
        correct += torch.eq(pred, y).sum().float().item()
    return correct / total


def main():
    model = ResNet18(5).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    best_acc, best_epoch = 0, 0
    global_step = 0
    viz.line([0], [-1], win='loss', opts=dict(title='loss'))
    viz.line([0], [-1], win='val_acc', opts=dict(title='val_acc'))

    for epoch in range(epoches):
        for step, (x, y) in enumerate(train_loader):
            # x:[b,3,224,224,] y:[b]
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = criterion(logits, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            viz.line([loss.item()], [global_step], win='loss', update='append')
            global_step += 1

        # validation
        if epoch % 1 == 0:
            val_acc = evalute(model, val_loader)
            if val_acc > best_acc:
                best_epoch = epoch
                best_acc = val_acc
                torch.save(model.state_dict(), 'best_for_scratch.mdl')  # 保存模型

                viz.line([val_acc], [global_step], win='val_acc', update='append')

    print('best acc: ', best_acc, ' best epoch: ', best_epoch)
    model.load_state_dict(torch.load('best_for_scratch.mdl'))
    print('loader from ckpt!')

    test_acc = evalute(model, test_loader)
    print('test acc:', test_acc)


if __name__ == '__main__':
    main()
